import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import streams.routing  # import our routing configuration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streamer.settings')
django.setup()  # Initialize Django

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(streams.routing.websocket_urlpatterns)
    )
})
