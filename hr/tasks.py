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

@shared_task()
def send_summary():
    data = RequestStatistics.objects.all()
    subject = "Звіт по запитам"
    message = ''
    for record in data:
        message += f'{record.user} send {record.requests} requests and have {record.exception} exceptions\n'
    send_mail(
        subject,
        message,
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )
