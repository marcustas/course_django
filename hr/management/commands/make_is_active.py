from django.core.management.base import BaseCommand

from hr.models import Employee

class Command(BaseCommand):
    help = 'Set "is_active" as True for all Employee'

    def handle(self, *args, **options):
        active = Employee.objects.filter(
            is_active=False
        )

        active.update(is_active=True)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully set "is_active" to True for all Employee',
            ),
        )
