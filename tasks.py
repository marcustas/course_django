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
    subject = "Password change is necessary"
    message_template = "Dear {}, please, change your password to {}."
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

        subject = f"Report on user activity {user.username}"
        message = f"User's name: {user.username}\nAmount of requests: {request_count}\nAmount of exceptions : {exception_count}"

        send_mail(
            subject,
            message,
            'from@example.com',
            ['admin@example.com'],
            fail_silently=False,
        )