from django.views.generic import TemplateView
from hr.models import Company



class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            company = Company.objects.first()
            if company.logo:
                context['logo'] = company.logo.url
            else:
                context['logo'] = '/static/img/logo.png'
        except Company.DoesNotExist:
            context['logo'] = '/static/img/logo.png'
        return context


