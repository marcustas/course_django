from django.core.management.base import BaseCommand
from hr.models import Employee


class Command(BaseCommand):
    help = 'Set "employee" is active'

    def handle(self, *args, **options):
        Employee.objects.update(is_active=True)

        self.stdout.write(
            self.style.SUCCESS(
                'Your employees is active now',
            ),
        )