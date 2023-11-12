from django.http import HttpResponse
from django.views import View

class RaiseExceptionView(View):
    def get(self, request):
        raise Exception("This is a test exception")
