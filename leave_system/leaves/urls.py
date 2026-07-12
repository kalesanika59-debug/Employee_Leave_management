from django.urls import path
from .views import (
    LeaveListCreateView, LeaveDetailView,
    dashboard, leave_list, leave_add, leave_edit, leave_delete,
    leave_approve, leave_reject
)

urlpatterns = [
    # REST API endpoints
    path('api/leaves/', LeaveListCreateView.as_view(), name='leave-list-create'),
    path('api/leaves/<int:pk>/', LeaveDetailView.as_view(), name='leave-detail'),

    # Normal HTML pages
    path('', dashboard, name='dashboard'),
    path('list/', leave_list, name='leave_list'),
    path('add/', leave_add, name='leave_add'),
    path('edit/<int:pk>/', leave_edit, name='leave_edit'),
    path('delete/<int:pk>/', leave_delete, name='leave_delete'),
    path('approve/<int:pk>/', leave_approve, name='leave_approve'),
    path('reject/<int:pk>/', leave_reject, name='leave_reject'),
]