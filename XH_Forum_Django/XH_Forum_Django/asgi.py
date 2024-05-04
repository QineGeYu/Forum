"""
ASGI config for XH_Forum_Django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
from . import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'XH_Forum_Django.settings')

#application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack( 
        URLRouter(
            routing.websocket_urlpatters
            )
        ),
})