from django.core.management.base import BaseCommand
from hr.models import Employee

class Command(BaseCommand):
    help = 'Make all employees active'

    def handle(self, *args, **options):
        Employee.objects.update(is_active=True)
        self.stdout.write(self.style.SUCCESS('All employees are now active.'))