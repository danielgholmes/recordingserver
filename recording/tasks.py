from datetime import datetime, timezone
import pathlib
import subprocess

from celery.task import task

from recording.models import Channel, Recording
from recordingserver.settings import RECORDING_DURATION


class RecordingError(Exception):
    pass


@task
def start_recordings():
    channels = Channel.objects.all().values()
    for channel in channels:
        record_channel(channel)


@task
def record_channel(channel):
    start_time = datetime.now(timezone.utc)
    start_time_formatted = start_time.strftime("%Y%m%d_%H%M%S")
    keyname = channel['keyname']
    channel_type = channel['channel_type']
    url = channel['url']

    path = f'recording_files/{channel_type}/{keyname}/'
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    if channel_type == Channel.TV:
        file_format = '.mp4'
        filename = f'{keyname}_server01_{start_time_formatted}{file_format}'
        ffmpeg_command = (f'ffmpeg -i "{url}" -r 10 -vcodec libx264 -movflags frag_keyframe -c:a aac -ab 48000 '
                          f'-ar 22050 -ac 1 -s 160x120 -t {RECORDING_DURATION} {path + filename}')
    elif channel_type == Channel.RADIO:
        file_format = '.aac'
        filename = f'{keyname}_server01_{start_time_formatted}{file_format}'
        ffmpeg_command = (f'ffmpeg -i "{url}" -c:a aac -ab 48000 -ar 22050 -ac 1 -t {RECORDING_DURATION} '
                          f'{path + filename}')
    else:
        raise RecordingError("Unknown channel type")

    try:
        subprocess.call(ffmpeg_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError as e:
        print("Streaming failed:", e)

    end_time = datetime.now(timezone.utc)
    recording = Recording(channel_id=channel['id'], start_time=start_time, end_time=end_time)
    recording.path = f'{channel_type}/{keyname}/{filename}'

    # check that the channel hasn't been deleted
    if Channel.objects.filter(id=channel['id']).first():
        recording.save()
    else:
        print('Channel deleted, recording not saved')
