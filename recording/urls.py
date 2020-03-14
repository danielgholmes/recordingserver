from django.urls import path

from .views import ChannelView, ChannelRecordingsView, RecordingView

app_name = "recording"

urlpatterns = [
    path('channel/', ChannelView.as_view()),
    path('channel/<int:pk>/', ChannelView.as_view()),
    path('channel/recordings/<int:pk>/', ChannelRecordingsView.as_view()),
    path('recordings/<int:pk>/', RecordingView.as_view(),)
]
