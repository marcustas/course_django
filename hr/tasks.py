from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Sum

from general.models import RequestStatistics
from hr.models import Employee
from django.utils import timezone
from datetime import timedelta


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
def generate_daily_report():
    yesterday = timezone.now() - timezone.timedelta(days=1)

    # Taking yesterday`s data or newer only
    user_statistics_list = RequestStatistics.objects.filter(
        timestamp__gte=yesterday
    ).values('user__username').annotate(
        requests=Sum('requests'),
        exception=Sum('exception')
    )

    # Forming report
    report = "Daily Report:\n"
    for user_statistics in user_statistics_list:
        report += (f"User: {user_statistics['user__username']}, "
                   f"Requests: {user_statistics['requests']}, "
                   f"Exceptions: {user_statistics['exception']}\n")

    # Sending report
    send_mail(
        'Daily Report',
        report,
        'from@example.com',
        ['admin1@example.com', 'admin2@example.com'],  # Адреса администраторов
        fail_silently=False,
    )
