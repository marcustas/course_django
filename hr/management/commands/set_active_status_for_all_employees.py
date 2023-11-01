from django.core.management.base import BaseCommand

from hr.models import Employee


class Command(BaseCommand):
    help = 'Set "active" status for all employees'  # noqa: A003

    def handle(self, *args, **kwargs):
        Employee.objects.update(is_active=True)

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully set Active status for All employees',
            ),
        )
