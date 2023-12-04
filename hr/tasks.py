
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
def generate_user_activity_report():
    data = RequestStatistics.objects.all()
    report = {}

    for entry in data:
        user_id = entry.user.id
        username = entry.user.username
        request_count = report.get(user_id, {}).get('request_count', 0) + 1
        exception_count = report.get(user_id, {}).get('exception_count', 0) + int(entry.has_exception)
        report[user_id] = {'username': username, 'request_count': request_count, 'exception_count': exception_count}
    report_text = "User Report:\n"

    for user_id, user_data in report.items():
        report_text += f"Username: {user_data['username']}, Requests: {user_data['request_count']}, Exceptions: {user_data['exception_count']}\n"
    subject = 'Daily Report'
    message = report_text
    from_email = 'your@email.com'
    admin_emails = list(Employee.objects.filter(is_superuser=True).values_list('email'))

    send_mail(
        subject,
        message,
        from_email,
        admin_emails,
        fail_silently=False,
    )