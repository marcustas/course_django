from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_django.settings')

app = Celery('course_django')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://redis:6379/0'
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
app.autodiscover_tasks()

# # configure Celery Beat schedule
# app.conf.beat_schedule = {
#     'generate_daily_report': {
#         'task': 'hr.tasks.generate_daily_report',
#         'schedule': crontab(hour='8', minute='0'),  # о 8:00 кожного дня
#     },
# }