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

    def clean(self):
        clean = super().clean()
        count_of_sick_days = list(clean.values()).count(WorkDayEnum.SICK_DAY.name)
        count_of_holiday_days = list(clean.values()).count(WorkDayEnum.HOLIDAY.name)

        if count_of_sick_days > 5:
            raise forms.ValidationError('No more than 5 sick days!')

        if count_of_holiday_days > 3:
            raise forms.ValidationError('No more than 3 holiday days!')

        return clean

    def clean_employee(self):
        clean = super().clean()
        employee = clean.get('employee')
        if not employee:
            raise forms.ValidationError("This field is required!")

        return employee
