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
        """
        Clean the employee field.

        This function calls the `clean()` method of the parent class to perform general cleaning operations.
        It then retrieves the value of the `employee` field from the cleaned data dictionary.

        If the `employee` field is empty or None, a `ValidationError` is raised with the message 'Заповніть поле'.

        Returns:
            str: The value of the `employee` field.

        Raises:
            forms.ValidationError: If the `employee` field is empty or None.
        """
        # Call the clean() method of the parent class and store the result in the 'clean' variable
        clean = super().clean()

        # Retrieve the value of the 'employee' field from the 'clean' dictionary
        employee = clean.get('employee')

        # If the 'employee' field is empty or None, raise a ValidationError with the message 'Заповніть поле'
        if not employee:
            raise forms.ValidationError('Заповніть поле')

        # Return the value of the 'employee' field
        return employee

    def clean_days(self):
        """
        Cleans the form data and validates the number of sick days and vacation days.

        Returns:
            dict: Cleaned form data.

        Raises:
            forms.ValidationError: If there are too many sick days or vacation days.
        """
        clean = super().clean()

        # Validate number of sick days
        sick_days = clean.get('sick days')
        if sick_days is not None and sick_days > 5:
            raise forms.ValidationError('Забагато днів для хвороби')

        # Validate number of vacation days
        vacation_days = clean.get('vacation days')
        if vacation_days is not None and vacation_days > 3:
            raise forms.ValidationError('Забагато днів для відпочинку')

        return clean