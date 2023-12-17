from celery import Celery
import os
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_django.settings')

app = Celery('course_django')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://redis:6379/0'
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-activity-report': {
        'task': 'path.to.send_activity_report',
        'schedule': timedelta(days=1),
        'args': (),
    },
}