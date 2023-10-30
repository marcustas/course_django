from django.urls import path

from examples.Homework_querystes import homework_querysets


urlpatterns = [
    path('querysets/', homework_querysets, name='homework_querystes'),
]
