from channels.routing import ProtocolTypeRouter, URLRouter,  ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from chat import routing as core_routing
import os
from chat import consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            core_routing.websocket_urlpatterns
        )
    ),
    "channel": ChannelNameRouter({
        "service-detection": consumers.ChatConsumer,
    }),
})