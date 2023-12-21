from rest_framework import serializers, status
from rest_framework.response import Response

from hr.models import Department, Employee, Position


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('name', 'parent_department')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'position',
        )


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = (
            'id',
            'title',
            'department',
            'is_manager',
            'is_active',
            'job_description',
            'monthly_rate',
        )


class SalarySerializer(serializers.Serializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )
    working_days = serializers.IntegerField()
    holiday_days = serializers.IntegerField()
    sick_days = serializers.IntegerField(default=0)
    vacation_days = serializers.IntegerField(default=0)
