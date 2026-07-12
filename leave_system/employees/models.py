from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    date_of_joining = models.DateField()

    def __str__(self):
        return f"{self.employee_id} - {self.name}"
