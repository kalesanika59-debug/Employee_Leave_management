from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = Leave
        fields = '__all__'

    def validate(self, data):
        if data['from_date'] > data['to_date']:
            raise serializers.ValidationError("From Date cannot be greater than To Date.")
        return data