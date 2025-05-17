from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/streams/<int:stream_id>/', consumers.StreamConsumer.as_asgi()),
]
