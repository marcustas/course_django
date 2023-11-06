from django.core.management.base import BaseCommand

from hr.models import Employee


class Command(BaseCommand):
    help = 'All employees are active'

    def handle(self, *args, **kwargs):
        Employee.objects.update(is_active=True)

        self.stdout.write(
            self.style.SUCCESS(
                'All employees are active success',
            ),
        )
