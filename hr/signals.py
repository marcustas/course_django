import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver

from hr.constants import MINIMUM_SALARY
from hr.models import Position


logger = logging.getLogger()


@receiver(pre_save, sender=Position)
def ensure_minimum_wage(sender, instance, **kwargs):
    if instance.monthly_rate < MINIMUM_SALARY:
        instance.monthly_rate = MINIMUM_SALARY
        logger.info(
            f"Заробітна плата для позиції '{instance.title}' була збільшена до мінімального порогу {MINIMUM_SALARY}.",
        )
