from django.urls import path

from .views import ChannelView

app_name = "recording"

urlpatterns = [
    path('channel/<int:pk>/', ChannelView.as_view()),
    path('channel/', ChannelView.as_view()),
]
