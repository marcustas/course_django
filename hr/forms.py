from django import forms
from django.core.exceptions import ValidationError

from hr.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('username', 'first_name', 'last_name', 'email', 'position', 'employee', 'sick_leave', 'holiday')

    def clean_employee(self):
        employee = self.cleaned_data.get('employee')
        if not employee:
            raise ValidationError("Поле Employee обязательно для заполнения.")
        return employee

    def clean_sick_leave(self):
        sick_leave = self.cleaned_data.get('sick_leave')
        if sick_leave > 5:
            raise ValidationError("Количество лікарняних днів не може бути більше 5.")
        return sick_leave

    def clean_holiday(self):
        holiday = self.cleaned_data.get('holiday')
        if holiday > 3:
            raise ValidationError("Кількість днів відпочинку не може бути більше 3.")
        return holiday
