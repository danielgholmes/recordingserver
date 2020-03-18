from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recordingserver.settings')

app = Celery('recording')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# configure celery beat that runs the periodic task of initiating recording threads
app.conf.beat_schedule = {
    "recording-task": {
        "task": "recording.tasks.start_recordings",
        "schedule": settings.RECORDING_DURATION - settings.RECORDING_OVERLAP
    }
}
