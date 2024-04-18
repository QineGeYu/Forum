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
from XH_Forum_webapp.views import show_post
from XH_Forum_webapp.views import show_user_post
from XH_Forum_webapp.views import show_user_message
from XH_Forum_webapp.views import search
from XH_Forum_webapp.views import like_post
from XH_Forum_webapp import views

urlpatterns = [
    path('api/login/', login_view, name='login'),
    path('api/register/', register_view, name='register'),
    path('api/show_post/',show_post, name='show_post'),
    path('api/show_user_post/',show_user_post, name='show_user_post'),
    path('api/show_user_message/',show_user_message, name='show_user_message'),
    path('api/search/', search, name='search'),
    path('like_post/',like_post,name='like_post'),
]