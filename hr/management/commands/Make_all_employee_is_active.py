from django.core.management.base import BaseCommand

from hr.models import Employee


class NewCommand(BaseCommand):
    help = 'Activate all employees'

    def all_employee_is_active(self):
        employees = Employee.objects.all()
        employees.update(is_active=True)

        self.stdout.write(self.style.SUCCESS('All employees have been activated.'))
