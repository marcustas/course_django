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
                Q(email__iexact=search)
            )
        return queryset


class EmployeeCreateView(UserPassesTestMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('employee_list')

    def test_func(self):
        return user_is_superadmin(self.request.user)


class EmployeeUpdateView(UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_form.html'
    success_url = reverse_lazy('employee_list')

    def test_func(self):
        return user_is_superadmin(self.request.user)


class EmployeeDeleteView(UserPassesTestMixin, DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

    def test_func(self):
        return user_is_superadmin(self.request.user)


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'Employee_detailed_view.html'

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        title = obj.position.title
        job_description = obj.position.job_description
        department = obj.position.department.name
        hire_date = obj.hire_date
        birth_date = obj.birth_date
        phone_number = obj.phone_number

        context = super().get_context_data(**kwargs)
        context['title'] = title
        context['job_description'] = job_description
        context['department'] = department
        context['hire_date'] = hire_date
        context['birth_date'] = birth_date
        context['phone_number'] = phone_number

        # context_to_merge = {
        #     'title': title,
        #     'job_description': job_description,
        #     'department': department,
        #
        # }
        # merged_context = context.update(context_to_merge)
        # return merged_context                                 # didn`t work that way for some reason (((
        return context

