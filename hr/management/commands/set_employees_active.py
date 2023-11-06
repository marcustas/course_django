from django.core.management.base import BaseCommand

from hr.models import Employee


class Command(BaseCommand):
    help = 'Update all employees to have an active status'

    def handle(self, *args, **kwargs):
        Employee.objects.update(is_active=True)

        self.stdout.write(self.style.SUCCESS('All employees have been set as active.'))
