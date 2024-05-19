"""XH_Forum_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from XH_Forum_webapp.views import login_view
from XH_Forum_webapp.views import register_view
from XH_Forum_webapp.views import getEmail
from XH_Forum_webapp.views import show_post
from XH_Forum_webapp.views import show_user_post
from XH_Forum_webapp.views import show_user_post2
from XH_Forum_webapp.views import show_user_message
from XH_Forum_webapp.views import show_user_message2
from XH_Forum_webapp.views import search
from XH_Forum_webapp.views import like_post
from XH_Forum_webapp.views import like_comment
from XH_Forum_webapp.views import publish_post
from XH_Forum_webapp.views import publish_singleMessage
from XH_Forum_webapp.views import get_post_detail
from XH_Forum_webapp.views import get_post_comments
from XH_Forum_webapp.views import publish_comment
from XH_Forum_webapp.views import save_contact
from XH_Forum_webapp.views import get_contacts
from XH_Forum_webapp.views import get_chat_messages
from XH_Forum_webapp.views import get_server_public_key
from XH_Forum_webapp.views import get_server_private_key
from XH_Forum_webapp.views import savePublicKey
from XH_Forum_webapp.views import verifyCode
from XH_Forum_webapp.views import resetPassword
from XH_Forum_webapp.views import update_post_privacy
from XH_Forum_webapp.views import edit_profile
from XH_Forum_webapp.views import get_avatar
from XH_Forum_webapp.views import get_avatar2
from XH_Forum_webapp import views

urlpatterns = [
    path('api/login/', login_view, name='login'),
    path('api/edit_profile/',edit_profile,name='edit_profile'),
    path('api/get_avatar/',get_avatar,name='get_avatar'),
    path('api/get_avatar2/<str:username>/',get_avatar2,name='get_avatar2'),
    path('api/register/', register_view, name='register'),
    path('api/getEmail/', getEmail, name='getEmail'),
    path('api/verifyCode/', verifyCode, name='verifyCode'),
    path('api/resetPassword/',resetPassword,name='resetPassword'),
    path('api/show_post/',show_post, name='show_post'),
    path('api/update_post_privacy/',update_post_privacy,name='update_post_privacy'),
    path('api/show_user_post/',show_user_post, name='show_user_post'),
    path('api/show_user_post2/',show_user_post2, name='show_user_post2'),
    path('api/show_user_message/',show_user_message, name='show_user_message'),
    path('api/show_user_message2/',show_user_message2, name='show_user_message2'),
    path('api/search/', search, name='search'),
    path('api/like_post/',like_post,name='like_post'),
    path('api/like_comment/',like_comment,name='like_comment'),
    path('api/publish_post/',publish_post,name='publish_post'),
    path('api/publish_singleMessage/',publish_singleMessage,name='publish_singleMessage'),
    path('api/posts/<int:post_id>/', get_post_detail, name='post_detail'),
    path('api/comments/<int:post_id>/', get_post_comments, name='get_post_comments'),
    path('api/publish_comment/',publish_comment,name='publish_comment'),
    path('api/save_contact/',save_contact,name='save_contact'),
    path('api/get_contacts/',get_contacts,name='get_contacts'),
    path('api/get_chat_messages/',get_chat_messages,name='get_chat_messages'),
    path('api/get_server_public_key/',get_server_public_key,name='get_server_public_key'),
    path('api/get_server_private_key/',get_server_private_key,name='get_server_private_key'),
    path('api/savePublicKey/',savePublicKey,name='savePublicKey')
]