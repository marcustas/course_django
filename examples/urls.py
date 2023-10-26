from django.urls import path

from examples.querysets import querysets_examples
from homework_query_sets import homework_query_sets


urlpatterns = [
    path('querysets/', querysets_examples, name='querysets_examples'),
    path('homework_querysets/', homework_query_sets, name='homework_query_sets'),
]
