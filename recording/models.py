from django.core.validators import MinLengthValidator
from django.db import models


class Channel(models.Model):
    RADIO = 'radio'
    TV = 'tv'
    CHANNEL_TYPES = (
        (RADIO, 'Radio'),
        (TV, 'TV')
        # add other channel types here
    )

    name = models.CharField(max_length=256)
    keyname = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    channel_type = models.CharField(max_length=16, choices=CHANNEL_TYPES)
    url = models.URLField()


def recordings_directory(instance, filename):
    return f'{instance.channel.channel_type}/{instance.channel.keyname}/{filename}'


class Recording(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    path = models.FileField(upload_to=recordings_directory)