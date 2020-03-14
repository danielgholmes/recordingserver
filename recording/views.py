from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from recording.models import Channel
from recording.serializers import ChannelSerializer


class ChannelView(APIView):
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
        return Response({"message": f"Channel {channel.name} with ID {channel.pk} deleted successfully"}, status=204)
