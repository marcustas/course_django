from django.core.management.base import BaseCommand

from hr.models import Employee

class Command(BaseCommand):
    help = 'Set is_active for all employees'

    def handle(self, *args, **kwargs):
        Employee.objects.update(is_active=True)

        self.stdout.write(
            self.style.SUCCESS(
                f'"is_active" has been set to "True" for all employees"',
            ),
        )
