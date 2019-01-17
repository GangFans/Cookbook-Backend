from django.urls import path
from . import views


app_name = 'Cookbook'

urlpatterns = [
    path('version', views.version, name='version'),
]
