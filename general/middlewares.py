import logging
from datetime import date
from django.utils.deprecation import MiddlewareMixin
from general.models import RequestStatistics
logger = logging.getLogger('middlewares')


class RequestStatisticsMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        logger.info('Called before view and get_response')
        response = self.get_response(request)
        logger.info('Called after view and get_response')
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and not request.path.startswith('/napshhdf/'):
            stats, created = RequestStatistics.objects.get_or_create(user=request.user)
            stats.requests += 1
            stats.save()

    def process_exception(self, request, exception):
        try:
            user = request.user
            stats, created = RequestStatistics.objects.get_or_create(user=user, date=date.today())
            stats.exceptions += 1
            stats.save()
        except RequestStatistics.DoesNotExist:
            pass
