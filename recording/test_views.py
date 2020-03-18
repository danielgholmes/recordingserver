import json

from django.test import TestCase
from model_bakery import baker

from recording.models import Channel, Recording


class ChannelViewTest(TestCase):
    """
    Test the CRUD operations for a channel
    """
    def test_get(self):
        channel = baker.make(Channel)
        response = self.client.get(f'/api/channel/{channel.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['channel']['name'], channel.name)
        self.assertEqual(response.json()['channel']['keyname'], channel.keyname)
        self.assertEqual(response.json()['channel']['channel_type'], channel.channel_type)
        self.assertEqual(response.json()['channel']['url'], channel.url)

    def test_post(self):
        self.assertEqual(Channel.objects.all().count(), 0)
        post_data = {
            "channel": {
                "name": "Test",
                "keyname": "test-chann",
                "channel_type": "tv",
                "url": "https://tv.com"
            }
        }
        response = self.client.post(f'/api/channel/', json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Channel.objects.all().count(), 1)
        channel = Channel.objects.all().first()
        self.assertEqual(channel.name, 'Test')
        self.assertEqual(channel.keyname, 'test-chann')
        self.assertEqual(channel.channel_type, 'tv')
        self.assertEqual(channel.url, 'https://tv.com')

    def test_put(self):
        channel = baker.make(Channel)
        put_data = {
            "channel": {
                "name": "Test",
                "keyname": "test-chann",
                "channel_type": "tv",
                "url": "https://tv.com"
            }
        }
        response = self.client.put(f'/api/channel/{channel.pk}/', json.dumps(put_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        channel.refresh_from_db()
        self.assertEqual(channel.name, 'Test')
        self.assertEqual(channel.keyname, 'test-chann')
        self.assertEqual(channel.channel_type, 'tv')
        self.assertEqual(channel.url, 'https://tv.com')

    def test_delete(self):
        channel = baker.make(Channel)
        response = self.client.delete(f'/api/channel/{channel.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Channel.objects.all().count(), 0)


class ChannelRecordingsViewTest(TestCase):
    """
    Test getting all the channel recording details
    """
    def test_get(self):
        channel = baker.make(Channel)
        baker.make(Recording, channel=channel, _quantity=2)
        response = self.client.get(f'/api/channel/recordings/{channel.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['recordings']), 2)
        self.assertEqual(response.json()['recordings'][0]['channel'], channel.pk)
        self.assertEqual(response.json()['recordings'][1]['channel'], channel.pk)


class RecordingViewTest(TestCase):
    """
    Test getting a recording detail
    """
    def test_get(self):
        recording = baker.make(Recording)
        response = self.client.get(f'/api/recording/{recording.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['recording']['channel'], recording.channel.pk)
        self.assertEqual(response.json()['recording']['path'], recording.path)

