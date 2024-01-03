from django.core.management.base import BaseCommand, CommandError

from hr.models import Employee


class Command(BaseCommand):
    help = 'Set all employees to active'

    def handle(self, *args, **options):
        try:
            Employee.objects.all().update(is_active=True)
            print('All employees are now active')
        except Exception as e:
            raise CommandError(e)
