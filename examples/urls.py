from django.urls import path

from examples.hw_querysets import hw_querysets
from examples.querysets import querysets_examples

urlpatterns = [
    path('querysets/', querysets_examples, name='querysets_examples'),
    path('homework_querysets/', hw_querysets, name='hw_querysets'),
]
