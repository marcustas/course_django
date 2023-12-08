from celery import shared_task
from django.core.mail import send_mail
from hr.models import Employee
from django.utils import timezone
from datetime import timedelta
from django.db import models
from general.models import RequestStatistics
@shared_task
def send_password_reset_emails():
    next_month = timezone.now().date() + timedelta(days=30)
    subject = "Зміна паролю необхідна"
    message_template = "Дорогий {}, будь ласка, змініть свій пароль до {}."

    for user in Employee.objects.all():
        message = message_template.format(user.username, next_month.strftime('%Y-%m-%d'))
        send_mail(
            subject,
            message,
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
@shared_task
def send_activity_report():
    yesterday = timezone.now().date() - timedelta(days=1)
    users = User.objects.all()

    for user in users:
        statistics, created = RequestStatistics.objects.get_or_create(
            user=user,
            date=yesterday
        )

        request_count = statistics.requests
        exception_count = statistics.exception

        subject = f"Звіт про активність користувача {user.username}"
        message = f"Ім'я користувача: {user.username}\nКількість запитів: {request_count}\nКількість винятків: {exception_count}"

        send_mail(
            subject,
            message,
            'from@example.com',
            ['admin@example.com'],
            fail_silently=False,
        )
