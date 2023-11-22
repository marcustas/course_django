import logging
from django.db.models.signals import pre_save
from django.dispatch import receiver

from hr.constants import MINIMUM_SALARY
from hr.models import (
    Position,
    Department,
)


logger = logging.getLogger()
@receiver(pre_save, sender=Position)
def ensure_minimum_wage(sender, instance, **kwargs):
    if instance.monthly_rate < MINIMUM_SALARY:
        instance.monthly_rate = MINIMUM_SALARY
        logger.info(
            f"Salary for the position '{instance.title}' was increased to the minimum threshold {MINIMUM_SALARY}.",
        )


@receiver(pre_save, sender=Department)
def capitalize_letter(sender, instance, **kwargs):
    instance.name = instance.name.capitalize()