from django.urls import path

from examples.querysets import querysets_examples


urlpatterns = [
    path('querysets/', querysets_examples, name='querysets_examples'),
]
