from rest_framework import serializers

from recording.models import Channel, Recording


class ChannelSerializer(serializers.ModelSerializer):
    """
    Serializer for the channel model
    """
    class Meta:
        model = Channel
        fields = ['name', 'keyname', 'channel_type', 'url']

    def create(self, validated_data):
        return Channel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.keyname = validated_data.get('keyname', instance.keyname)
        instance.channel_type = validated_data.get('channel_type', instance.channel_type)
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance


class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = ['channel', 'start_time', 'end_time', 'path']

