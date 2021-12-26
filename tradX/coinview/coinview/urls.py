"""
Definition of urls for coinview.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from app import forms, views
from .settings import STATIC_URL
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', views.loginView, name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('history', views.history, name='history'),
    path('admin/', admin.site.urls),
]
