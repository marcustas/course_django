from django.views.generic import TemplateView
from hr.models import Company

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_data = Company.objects.first()
        context['company'] = company_data
        return context