from django.core.management.base import BaseCommand
from hr.models import Employee


class Command(BaseCommand):
    help = "Mark all employees as active"

    def handle(self, *args, **kwargs):
        try:
            Employee.objects.update(is_active=True)
            self.stdout.write(self.style.SUCCESS("All employees are marked active"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

