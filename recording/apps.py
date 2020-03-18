from django.apps import AppConfig


class RecordingConfig(AppConfig):
    name = 'recording'

    def ready(self):
        from recording.tasks import start_recordings
        start_recordings.delay()
