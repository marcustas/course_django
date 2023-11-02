import logging

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

    def process_view(self, request, _, __, ___):
        """
        Process the view to update request statistics for authenticated users.

        Args:
            request (HttpRequest): The request object.
        """
        try:
            # Check if the user is authenticated and the path does not start with '/napshhdf/'
            if request.user.is_authenticated and not request.path.startswith('/napshhdf/'):
                # Get or create the request statistics object for the user
                stats, _ = RequestStatistics.objects.get_or_create(user=request.user)
                # Increment the requests count
                stats.requests += 1
                # Save the updated statistics
                stats.save()
        except RequestStatistics.DoesNotExist:
            pass

    def process_exception(self, request, _):
        """
        Process an exception that occurred during request processing.

        Args:
            request (HttpRequest): The request object.
            _ (Exception): The exception object (not used in this function).
        """
        try:
            # Get the user from the request object
            user = request.user

            # Get or create the RequestStatistics object for the user
            stats, _ = RequestStatistics.objects.get_or_create(user=user)

            # Increment the exception count
            stats.exceptions += 1

            # Save the updated statistics
            stats.save()
        except RequestStatistics.DoesNotExist:
            # Ignore the exception if the RequestStatistics object does not exist
            pass
