from django.views.generic import TemplateView

from hr.models import Company


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """
        Override the get_context_data method to add additional context data.
        """
        # Call the parent's get_context_data method to get the initial context
        context = super().get_context_data(**kwargs)

        # Add the Company.objects.first() to the context
        context['company'] = Company.objects.first()

        # Return the updated context
        return context
