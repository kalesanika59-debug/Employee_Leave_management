from rest_framework import generics, serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from employees.models import Employee
from .models import Leave

# ---------- Serializer (converts Leave model data to/from JSON) ----------

class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = Leave
        fields = '__all__'

    def validate(self, data):
        if data['from_date'] > data['to_date']:
            raise serializers.ValidationError("From Date cannot be greater than To Date.")
        return data

# ---------- REST API Views (DRF) ----------

class LeaveListCreateView(generics.ListCreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'leave_type']

class LeaveDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

# ---------- Normal HTML Views (browser pages) ----------

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')
def dashboard(request):
    context = {
        'total_employees': Employee.objects.count(),
        'total_leaves': Leave.objects.count(),
        'pending': Leave.objects.filter(status='Pending').count(),
        'approved': Leave.objects.filter(status='Approved').count(),
        'rejected': Leave.objects.filter(status='Rejected').count(),
    }
    return render(request, 'leaves/dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')
def leave_list(request):
    leaves = Leave.objects.all()

    # Search by employee name or employee ID
    query = request.GET.get('q', '')
    if query:
        leaves = leaves.filter(employee__name__icontains=query) | leaves.filter(employee__employee_id__icontains=query)

    # Filter by status or leave type
    status = request.GET.get('status', '')
    if status:
        leaves = leaves.filter(status=status)

    leave_type = request.GET.get('leave_type', '')
    if leave_type:
        leaves = leaves.filter(leave_type=leave_type)

    return render(request, 'leaves/leave_list.html', {
        'leaves': leaves, 'query': query, 'status': status, 'leave_type': leave_type
    })
@login_required
def leave_add(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None

    is_hr = request.user.is_staff or request.user.is_superuser
    employees = Employee.objects.all() if is_hr else None

    if request.method == 'POST':
        if is_hr:
            employee = get_object_or_404(Employee, pk=request.POST['employee'])
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        if from_date > to_date:
            return render(request, 'leaves/leave_form.html', {
                'employees': employees,
                'is_hr': is_hr,
                'error': 'From Date cannot be greater than To Date.'
            })

        Leave.objects.create(
            employee=employee,
            leave_type=request.POST['leave_type'],
            from_date=from_date,
            to_date=to_date,
            reason=request.POST['reason'],
            status='Pending',
        )
        return redirect('leave_list' if is_hr else 'employee_dashboard')

    return render(request, 'leaves/leave_form.html', {'employees': employees, 'is_hr': is_hr})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')
def leave_edit(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    employees = Employee.objects.all()
    if request.method == 'POST':
        leave.employee = get_object_or_404(Employee, pk=request.POST['employee'])
        leave.leave_type = request.POST['leave_type']
        leave.from_date = request.POST['from_date']
        leave.to_date = request.POST['to_date']
        leave.reason = request.POST['reason']
        leave.status = request.POST['status']
        leave.save()
        return redirect('leave_list')
    return render(request, 'leaves/leave_form.html', {'leave': leave, 'employees': employees})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')
def leave_delete(request, pk):
    get_object_or_404(Leave, pk=pk).delete()
    return redirect('leave_list')


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')
def leave_approve(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    leave.status = 'Approved'
    leave.save()
    return redirect('leave_list')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='login')
def leave_reject(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    leave.status = 'Rejected'
    leave.save()
    return redirect('leave_list')