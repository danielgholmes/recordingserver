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

    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'keyname')

    def __str__(self):
        return f'{self.keyname}'


class Recording(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    path = models.CharField(max_length=256)

    class Meta:
        ordering = ('channel', 'start_time')
        unique_together = ('channel', 'path')

    def __str__(self):
        return f'{self.path} for channel {self.channel}'
