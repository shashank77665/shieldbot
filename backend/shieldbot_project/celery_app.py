import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shieldbot_project.settings')

app = Celery('shieldbot_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Optionally, you can override broker settings here if needed:
app.conf.broker_url = 'redis://127.0.0.1:6379/0'
app.conf.result_backend = 'redis://127.0.0.1:6379/0'
