import calendar
from datetime import date

from django import forms
from django.forms import ChoiceField

from common.enums import WorkDayEnum
from hr.models import Employee


WorkDayChoices = [(tag.name, tag.value) for tag in WorkDayEnum]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('username', 'first_name', 'last_name', 'email', 'position')


class SalaryForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())

    def __init__(self, *args, **kwargs):
        super(SalaryForm, self).__init__(*args, **kwargs)

        today = date.today()
        _, num_days = calendar.monthrange(today.year, today.month)

        for day in range(1, num_days + 1):
            weekday_name = calendar.day_name[calendar.weekday(today.year, today.month, day)]
            field_name = f'day_{day}'

            if calendar.weekday(today.year, today.month, day) >= 5:  # Saturday and Sunday
                self.fields[field_name] = ChoiceField(
                    label=f'{day} - {weekday_name}',
                    choices=[(WorkDayEnum.WEEKEND.name, WorkDayEnum.WEEKEND.value)],
                    initial=WorkDayEnum.WEEKEND.name,
                )
            else:
                self.fields[field_name] = ChoiceField(
                    label=f'{day} - {weekday_name}',
                    choices=WorkDayChoices,
                    initial=WorkDayEnum.WORKING_DAY.name,
                )

    def clean_employee(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')
        if not employee or employee is None:
            raise forms.ValidationError('Заповніть поле "Employee"')
        return employee

    def clean_days(self):
        cleaned_data = super().clean()
        sick_days = list(cleaned_data.values()).count('SICK_DAY')
        if sick_days is not None and sick_days > 5:
            raise forms.ValidationError('Лікарняних має бути менше ніж 6')

        vacation_days = list(cleaned_data.values()).count('HOLIDAY')
        if vacation_days is not None and vacation_days > 3:
            raise forms.ValidationError('Вихідних має бути менше ніж 4')

        return cleaned_data
