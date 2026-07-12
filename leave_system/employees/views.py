import uuid
from rest_framework import generics, serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Employee

# ---------- Serializer ----------

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

# ---------- REST API Views (DRF) ----------

class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# ---------- Auth Views ----------

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('dashboard')            # HR Dashboard
            else:
                return redirect('employee_dashboard')    # Employee Dashboard
        else:
            return render(request, 'employees/login.html', {'error': 'Invalid username or password'})
    return render(request, 'employees/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
def register_view(request):
    if request.method == 'POST':
        employee_id = request.POST['employee_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'employees/register.html', {'error': 'Passwords do not match.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'employees/register.html', {'error': 'Username already taken.'})

        if Employee.objects.filter(email=email).exists():
            return render(request, 'employees/register.html', {'error': 'Email already registered.'})

        if Employee.objects.filter(employee_id=employee_id).exists():
            return render(request, 'employees/register.html', {'error': 'Employee ID already registered.'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=False
        )

        Employee.objects.create(
            user=user,
            employee_id=employee_id,
            name=f"{first_name} {last_name}",
            email=email,
            department="Not Assigned",
            mobile_number=mobile_number,
            date_of_joining=timezone.now().date(),
        )

        login(request, user)
        return redirect('employee_dashboard')

    return render(request, 'employees/register.html')

@login_required
def employee_dashboard(request):
    from leaves.models import Leave
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        employee = None
    leaves = Leave.objects.filter(employee=employee) if employee else []
    return render(request, 'employees/employee_dashboard.html', {'employee': employee, 'leaves': leaves})

# ---------- Normal HTML Views (browser pages) ----------

@login_required
def employee_list(request):
    query = request.GET.get('q', '')
    employees = Employee.objects.filter(name__icontains=query) if query else Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees, 'query': query})

@login_required
def employee_add(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        user = User.objects.get(pk=user_id) if user_id else None
        Employee.objects.create(
            user=user,
            employee_id=request.POST['employee_id'],
            name=request.POST['name'],
            email=request.POST['email'],
            department=request.POST['department'],
            mobile_number=request.POST['mobile_number'],
            date_of_joining=request.POST['date_of_joining'],
        )
        return redirect('employee_list')
    users = User.objects.filter(is_staff=False)
    return render(request, 'employees/employee_form.html', {'users': users})

@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        user_id = request.POST.get('user')
        employee.user = User.objects.get(pk=user_id) if user_id else None
        employee.name = request.POST['name']
        employee.email = request.POST['email']
        employee.department = request.POST['department']
        employee.mobile_number = request.POST['mobile_number']
        employee.date_of_joining = request.POST['date_of_joining']
        employee.save()
        return redirect('employee_list')
    users = User.objects.filter(is_staff=False)
    return render(request, 'employees/employee_form.html', {'employee': employee, 'users': users})

@login_required
def employee_delete(request, pk):
    get_object_or_404(Employee, pk=pk).delete()
    return redirect('employee_list')

def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password != confirm_password:
            return render(request, 'employees/forgot_password.html', {'error': 'Passwords do not match.'})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'employees/forgot_password.html', {'error': 'Username not found.'})

        user.set_password(new_password)
        user.save()
        return render(request, 'employees/forgot_password.html', {'success': 'Password changed successfully! You can now login with your new password.'})

    return render(request, 'employees/forgot_password.html')