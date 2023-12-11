from celery import shared_task
from django.core.mail import send_mail
from hr.models import Employee
from django.utils import timezone
from datetime import timedelta
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
def generate_activity_report():
    subject = "User Activity Report"
    message_template = "User: {}, Requests: {}, Exceptions: {}"
    user_data = RequestStatistics.objects.all()

    for user in user_data:
        report = "\n".join(
            message_template.format(user.username, user.request_count, user.exception_count)
        )
        send_mail(
            subject,
            report,
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
