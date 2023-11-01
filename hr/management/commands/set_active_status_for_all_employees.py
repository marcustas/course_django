from django.core.management.base import BaseCommand

from hr.models import Employee


class Command(BaseCommand):
    help = 'Set "active" status for all Employees'

    def handle(self, *args, **kwargs):
        employees = Employee.objects.update(is_active=True)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully set "active" status for {employees.count()} Employees',
            ),
        )
