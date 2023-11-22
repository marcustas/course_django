from rest_framework import serializers

from hr.constants import MAX_MONTH_DAYS
from hr.models import (
    Employee,
    Position, Department,
)
from hr.validators import validate_positive, validate_max_month_days
from static.CONSTANS import SICK_DAYS_MAX, HOLIDAYS_DAYS_MAX


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'position')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'title', 'department', 'is_manager', 'is_active', 'job_description', 'monthly_rate')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class SalarySerializer(serializers.Serializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    working_days = serializers.IntegerField(validators=[validate_positive, validate_max_month_days], max_value=31)
    holiday_days = serializers.IntegerField(validators=[])
    sick_days = serializers.IntegerField(default=0)
    vacation_days = serializers.IntegerField(default=0)

    def validate(self, data):
        total_days = sum([
            data.get('working_days', 0),
            data.get('holiday_days', 0),
            data.get('sick_days', 0),
            data.get('vacation_days', 0),
        ])
        if total_days > MAX_MONTH_DAYS:
            raise serializers.ValidationError('Total days exceed the number of days in a month.')
        return data

    def validate_sick_days(self, value):
        """
        Checks that the number of sick days does not exceed 3.
        """
        if value > SICK_DAYS_MAX:
            raise serializers.ValidationError(f'The number of sick days cannot be more than {SICK_DAYS_MAX}.')
        return value

    def validate_holiday_days(self, value):
        """
        Checks that the number of holiday days does not exceed 5.
        """
        if value > HOLIDAYS_DAYS_MAX:
            raise serializers.ValidationError(f'The number of sick holiday cannot be more than {HOLIDAYS_DAYS_MAX}.')
        return value