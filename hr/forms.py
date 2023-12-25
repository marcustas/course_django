from django import forms

from hr.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("username", "first_name", "last_name", "email", "position")
