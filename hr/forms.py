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
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False)

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
        employee = self.cleaned_data['employee']
        if not employee:
            raise forms.ValidationError('Employee is required.')
        return employee

    def clean(self):
        cleaned_data = super().clean()

        seek_days_count = sum(1 for field_name, value in cleaned_data.items() if value == WorkDayEnum.SICK_DAY.name)
        holiday_days_count = sum(1 for field_name, value in cleaned_data.items() if value == WorkDayEnum.HOLIDAY.name)

        if seek_days_count > 5:
            raise forms.ValidationError('Sick days count cannot be more than 5.')
        if holiday_days_count > 3:
            raise forms.ValidationError('Holiday days count cannot be more than 3.')
