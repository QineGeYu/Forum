from django.urls import re_path
from XH_Forum_webapp import consumers
websocket_urlpatters = {
    #re_path(r'chat/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path('chat/', consumers.ChatConsumer.as_asgi()),
}
