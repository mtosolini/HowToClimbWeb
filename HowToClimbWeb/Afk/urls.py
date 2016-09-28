"""Defines url pattern for Afk"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # Test
    url(r'^$', views.index, name='index'),
    url(r'^afk/(?P<summonername>[\w\s]+)$', views.countAfk),
    ]