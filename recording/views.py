from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from recording.models import Channel, Recording
from recording.serializers import ChannelSerializer, RecordingSerializer


class ChannelView(APIView):
    """
    View for all CRUD operations on a channel
    """
    def get(self, request, pk):
        channels = Channel.objects.all()
        channel = get_object_or_404(channels, pk=pk)
        serializer = ChannelSerializer(channel)
        return Response({"channel": serializer.data})

    def post(self, request):
        channel = request.data.get('channel')
        serializer = ChannelSerializer(data=channel)
        if serializer.is_valid(raise_exception=True):
            channel = serializer.save()
        return Response({"success": f"Channel {channel.name} with ID {channel.pk} created successfully"})

    def put(self, request, pk):
        channels = Channel.objects.all()
        channel = get_object_or_404(channels, pk=pk)
        data = request.data.get('channel')
        serializer = ChannelSerializer(instance=channel, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            channel = serializer.save()
        return Response({"success": f"Channel {channel.name} with ID {channel.pk} updated successfully"})

    def delete(self, request, pk):
        channels = Channel.objects.all()
        channel = get_object_or_404(channels, pk=pk)
        channel.delete()
        return Response({"message": f"Channel {channel.name} with ID {pk} deleted successfully"}, status=204)


class ChannelRecordingsView(APIView):
    """
    View that gets all of the recordings associated with a channel
    """
    def get(self, request, pk):
        channels = Channel.objects.all()
        channel = get_object_or_404(channels, pk=pk)
        recordings = channel.recording_set.all()
        serializer = RecordingSerializer(recordings, many=True)
        return Response({"recordings": serializer.data})


class RecordingView(APIView):
    """
    View to get a single recording from a channel
    """
    def get(self, request, pk):
        recordings = Recording.objects.all()
        recording = get_object_or_404(recordings, pk=pk)
        serializer = RecordingSerializer(recording)
        return Response({"recording": serializer.data})
