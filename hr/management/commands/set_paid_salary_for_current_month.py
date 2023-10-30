from django.core.management.base import BaseCommand
from django.utils import timezone

from hr.models import MonthlySalary


class Command(BaseCommand):
    help = 'Set "paid" as True for all MonthlySalary instances where month_year is the current month'  # noqa: A003

    def handle(self, *args, **kwargs):
        current_month = timezone.now().month
        current_year = timezone.now().year

        # Filter the MonthlySalary instances by current month and year
        salaries = MonthlySalary.objects.filter(
            month_year__month=current_month,
            month_year__year=current_year,
            paid=False,
        )

        # Update the "paid" field for the filtered instances
        salaries.update(paid=True)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully set "paid" to True for {salaries.count()} MonthlySalary instances for the current month',
            ),
        )
