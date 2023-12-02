from django.core.management.base import BaseCommand
from myapp.models import Employee


class Command(BaseCommand):
    help = 'Activate all employees'

    def handle(self, *args, **kwargs):
        Employee.objects.all().update(is_active=True)
        self.stdout.write(
            self.style.SUCCESS('Successfully activated all employees')
        )
