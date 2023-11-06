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
    max_sick_days = 5
    max_holiday_days = 3

    def __init__(self, *args, **kwargs):
        super(SalaryForm, self).__init__(*args, **kwargs)

        today = date.today()
        _, self.num_days = calendar.monthrange(today.year, today.month)

        for day in range(1, self.num_days + 1):
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

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')

        if not employee:
            raise forms.ValidationError("'Employee' field cannot be empty.")

        sick_leave_days = sum(cleaned_data.get(f'day_{day}') == 'SICK_DAY' for day in range(1, self.num_days + 1))
        holiday_days = sum(cleaned_data.get(f'day_{day}') == 'HOLIDAY' for day in range(1, self.num_days + 1))

        if sick_leave_days > self.max_sick_days:
            raise forms.ValidationError(f"The number of sick leaves should not exceed {self.max_sick_days}.")

        if holiday_days > self.max_holiday_days:
            raise forms.ValidationError(f"The number of holidays should not exceed {self.max_holiday_days}.")
