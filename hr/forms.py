import calendar
from datetime import date

from django import forms
from django.core.exceptions import ValidationError
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

    def clean(self):
        cleaned_data = super().clean()

        employee = cleaned_data.get('employee')
        if not employee:
            raise ValidationError("Поле 'Employee' обязательно для заполнения.")

        sick_leave_days = [cleaned_data.get(f'day_{day}') for day in range(1, 32)]
        if sick_leave_days.count(WorkDayEnum.SICK_DAY.name) > 5:
            raise ValidationError("Кількість лікарняних днів не повинна перевищувати 5.")

        holiday_days = [cleaned_data.get(f'day_{day}') for day in range(1, 32)]
        if holiday_days.count(WorkDayEnum.HOLIDAY.name) > 3:
            raise ValidationError("Кількість днів відпочинку не повинна перевищувати 3.")

        return cleaned_data
