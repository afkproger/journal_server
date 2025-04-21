import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import server.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journal.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(server.routing.websocket_urlpatterns),
})