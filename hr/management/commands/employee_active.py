from django.core.management.base import BaseCommand

from hr.models import Employee


class Command(BaseCommand):
    help = 'Mark all employees as active'

    def handle(self, *args, **kwargs):
        """
        This function is responsible for marking all employees as active.
        It takes in variable length arguments and arbitrary keyword arguments.

        It does not return anything.

        If an error occurs while updating the employees' status, it raises an exception.

        """
        try:
            # Update the is_active field of all Employee objects to True
            Employee.objects.update(is_active=True)

            # Print a success message to the console
            self.stdout.write(self.style.SUCCESS('All employees are marked active'))

        except Exception as e:
            # Print an error message to the console along with the error details
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
