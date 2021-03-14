from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/realtime/(?P<key>\S+)/$', consumers.RealtimeColorConsumer.as_asgi())
]