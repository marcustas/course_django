from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView,
)

from hr.forms import EmployeeForm
from hr.models import Employee


def user_is_superadmin(user) -> bool:
    return user.is_superuser


class EmployeeListView(ListView):
    model = Employee
    paginate_by = 10
    template_name = 'employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(position__title__icontains=search) |
                Q(email__iexact=search) |
                Q(email__icontains="gmail.com")
            )
        return queryset

    class EmployeeDetailView(DetailView):
        model = Employee
        template_name = 'Employee_detailed_view.html'
        context_object_name = 'employee'  # Optionally set a custom context variable name

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # You can access the attributes of the 'employee' object directly
            context['title'] = self.object.position.title
            context['job_description'] = self.object.position.job_description
            context['department'] = self.object.position.department.name
            context['hire_date'] = self.object.hire_date
            context['birth_date'] = self.object.birth_date
            context['phone_number'] = self.object.phone_number
            return context
