from django.core.management.base import BaseCommand

from hr.models import Employee


class Command(BaseCommand):
    help = 'Set all employees as active (is_active=True)'

    def handle(self, *args, **kwargs):
        Employee.objects.update(is_active=True)

        self.stdout.write(self.style.SUCCESS('All employees have been set as active.'))
