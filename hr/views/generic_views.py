from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView
)
from django.views import View
from django.http import JsonResponse

from hr.forms import EmployeeForm
from hr.models import Employee, Department, Position


def user_is_superadmin(user) -> bool:
    return user.is_superuser


class EmployeeListView(ListView):
    paginate_by = 10
    model = Employee
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
                Q(email__icontains=search),
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


class EmployeeProfileView(UserPassesTestMixin, DetailView):
    model = Employee
    template_name = 'employee_profile.html'

    def test_func(self):
        return user_is_superadmin(self.request.user)


class homework_querysets(View):
    def get(self, request, *args, **kwargs):
        # Запит 1
        departments_with_managers = Department.objects.filter(position__is_manager=True).order_by('name')

        # Запит 2
        total_active_positions = Position.objects.filter(is_active=True).count()

        # Запит 3
        hr_department = Department.objects.get(name="HR")
        positions_active_or_hr = Position.objects.filter(Q(is_active=True) | Q(department=hr_department))

        # Запит 4
        departments_with_managers_names = Department.objects.filter(position__is_manager=True).values('name')

        # Запит 5
        sorted_positions = Position.objects.order_by('title').values('title', 'is_active')

        data = {
            'departments_with_managers': list(departments_with_managers.values('name')),
            'total_active_positions': total_active_positions,
            'positions_active_or_hr': list(positions_active_or_hr.values('title')),
            'departments_with_managers_names': list(departments_with_managers_names),
            'sorted_positions': list(sorted_positions),
        }

        return JsonResponse(data)
