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
    # Отримання статистики для користувачів з можливістю відображення нульових значень для тих, у кого немає статистики
    user_stats = RequestStatistics.objects.values('employee__username', 'requests', 'exceptions')
    users_without_stats = Employee.objects.filter(request_statistics__isnull=True).values_list('username', flat=True)

    user_activity_report = []
    for stats in user_stats:
        user_activity_report.append({
            'username': stats['employee__username'],
            'requests_count': stats['requests'],
            'exceptions_count': stats['exceptions'],
        })

    for username in users_without_stats:
        user_activity_report.append({
            'username': username,
            'requests_count': 0,
            'exceptions_count': 0,
        })

    report_text = "User Activity Report:\n\n"
    for user_data in user_activity_report:
        report_text += f"Username: {user_data['username']}\nRequests Count: {user_data['requests_count']}\nExceptions Count: {user_data['exceptions_count']}\n\n"

    admin_emails = [admin.email for admin in Employee.objects.filter(is_superuser=True)]

    send_mail(
        'Daily User Activity Report',
        report_text,
        'from@example.com',
        admin_emails,
        fail_silently=False,
    )