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
        """
        Clean the form data and perform validation.

        Returns:
            dict: The cleaned form data.

        Raises:
            forms.ValidationError: If there are too many sick days or holiday days.
        """
        # Clean the form data
        cleaned_data = super().clean()

        # Count the number of sick days and holiday days
        count_of_sick_days = list(cleaned_data.values()).count(WorkDayEnum.SICK_DAY.name)
        count_of_holiday_days = list(cleaned_data.values()).count(WorkDayEnum.HOLIDAY.name)

        # Define the error message template
        error_text = 'No more than {} {} days!'

        # Check if there are too many sick days
        if count_of_sick_days > 5:
            raise forms.ValidationError(error_text.format(5, 'sick'))

        # Check if there are too many holiday days
        if count_of_holiday_days > 3:
            raise forms.ValidationError(error_text.format(3, 'holiday'))

        # Return the cleaned form data
        return cleaned_data

    def clean_employee(self):
        # Call the parent class's clean method to get the cleaned data
        cleaned_data = super().clean()

        # Get the employee value from the cleaned data
        employee = cleaned_data.get('employee')

        # If the employee value is not provided, raise a validation error
        if not employee:
            raise forms.ValidationError('This field is required!')

        # Return the employee value
        return employee
