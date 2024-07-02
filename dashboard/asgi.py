# """
# ASGI config for dashboard project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application


# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import channel.routing

# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

# # application = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             channel.routing.websocket_urlpatterns
#         )
#     ),
# })


# asgi.py


import os
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from django.urls import path,re_path

from channel.consumers import AlertConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sathi.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                # path('ws/chat/<str:username>/', ChatConsumer.as_asgi()),
                re_path(r'ws/alerts/$', AlertConsumer.as_asgi()),
            ]
        )
    ),
})