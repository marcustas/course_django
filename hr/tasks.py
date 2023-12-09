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
def send_report():
    statistic_data = RequestStatistics.objects.all()
    report = []
    for data in statistic_data:
        user = data.user
        request_count = data.request
        exception_count = data.exception
        report_part = [user, request_count, exception_count]
        report.append(report_part)

    final_report = "\n".join([f"{user} has {request_count} requests and {exception_count} exceptions" for user, request_count, exception_count in report])
    send_to = list(Employee.objects.filter(is_superuser=True).values_list('email', flat=True))
    send_mail(
        subject='Request Statistic Report',
        from_email="test@email.com",
        recipient_list=send_to,
        message=f"Hello, it is your daily report:{final_report}"
    )
