import datetime
import os
import pathlib

from celery.task import task

from recording.models import Channel, Recording


class RecordingError(Exception):
    pass


@task
def start_recordings():
    channels = Channel.objects.all().values()
    for channel in channels:
        record_channel(channel)


@task
def record_channel(channel):
    start_time = datetime.datetime.now()
    start_time_formatted = start_time.strftime("%Y%m%d_%H%M%S")
    keyname = channel['keyname']
    channel_type = channel['channel_type']
    url = channel['url']

    path = f'recording_files/{channel_type}/{keyname}/'
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    if channel_type == Channel.TV:
        file_format = '.mp4'
        filename = f'{keyname}_server01_{start_time_formatted}{file_format}'
        print(path + filename)
        ffmpeg_command = (f'ffmpeg -i "{url}" -r 10 -vcodec libx264 -movflags frag_keyframe -c:a aac -ab 48000 '
                          f'-ar 22050 -ac 1 -s 160x120 -t 3 {path + filename}')
    elif channel_type == Channel.RADIO:
        file_format = '.aac'
        filename = f'{keyname}_server01_{start_time_formatted}{file_format}'
        print(path + filename)
        ffmpeg_command = f'ffmpeg -i "{url}" -c:a aac -ab 48000 -ar 22050 -ac 1 -t 3 {path + filename}'
    else:
        raise RecordingError("Unknown channel type")

    os.system(ffmpeg_command)  # TODO potentially find a way to determine if successful

    end_time = datetime.datetime.now()
    recording = Recording(channel_id=channel['id'], start_time=start_time, end_time=end_time)
    recording.path = f'{recording.channel.channel_type}/{recording.channel.keyname}/{filename}'
    recording.save()


