from django.urls import path

from examples.homework_querysets import homework_querysets
from examples.querysets import querysets_examples


urlpatterns = [
    path('querysets/', querysets_examples, name='querysets_examples'),
    path('hw/', homework_querysets, name='homework_querysets'),
]
