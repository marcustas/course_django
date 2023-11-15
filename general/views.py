from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        company_instance = Company.objects.first()

        context['logo'] = company_instance.logo if company_instance else None

        return context


