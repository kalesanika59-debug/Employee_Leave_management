from django.db import models

# Create your models here.
from employees.models import Employee

class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Casual', 'Casual'),
        ('Sick', 'Sick'),
        ('Earned', 'Earned'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type} ({self.status})"