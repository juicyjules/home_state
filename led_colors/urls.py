"""home_state URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('master', views.master, name='master'),
    path('client', views.clients, name='clients'),
    path('color', views.colors, name='colors'),
    path('client/create', views.create_client, name='create_client'),
    path('client/<str:key>/info', views.client_info, name='client_info'),
    path('client/<str:key>/toggle', views.client_toggle, name='client_toggle'),
    path('client/<str:key>', views.client_edit, name='client_edit'),
    path('color/create', views.create_color, name='create_color'),
    path('color/<str:name>', views.edit_color, name='edit_color'),
]
    