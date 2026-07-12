from django.urls import path
from .views import (
    EmployeeListCreateView, EmployeeDetailView,
    employee_list, employee_add, employee_edit, employee_delete,
    login_view, logout_view, employee_dashboard, register_view,
    forgot_password_view
)

urlpatterns = [
    path('api/employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('api/employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('', employee_list, name='employee_list'),
    path('add/', employee_add, name='employee_add'),
    path('edit/<int:pk>/', employee_edit, name='employee_edit'),
    path('delete/<int:pk>/', employee_delete, name='employee_delete'),
    path('my-dashboard/', employee_dashboard, name='employee_dashboard'),
    path('register/', register_view, name='register'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
]