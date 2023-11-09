from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetView as BasePasswordResetView,
)
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme


class LoginView(BaseLoginView):
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return next_url

        return reverse_lazy('home')


class PasswordResetView(BasePasswordResetView):
    email_template_name = 'password_reset_email.txt'
    html_email_template_name = 'password_reset_email.html'
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'password_reset_confirm.html'
