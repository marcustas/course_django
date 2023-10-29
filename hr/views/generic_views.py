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

from hr.forms import EmployeeForm
from hr.models import Employee

from django.shortcuts import render
from hr.models import Department, Position


def homework_querysets(request):
    departments_with_managers = Department.objects.filter(position__is_manager=True).order_by('name')

    total_active_positions = Position.objects.filter(is_active=True).count()

    positions_active_or_hr = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))

    departments_with_managers_names = Department.objects.filter(position__is_manager=True).values('name')

    positions_sorted = Position.objects.order_by('title').values('title', 'is_active')

    # Виводимо результати в консоль
    print("Запит 1 - Відділи з позиціями менеджерів:")
    for department in departments_with_managers:
        print(department.name)

    print("Запит 2 - Загальна кількість активних позицій:", total_active_positions)

    print("Запит 3 - Позиції, які є активними або належать до відділу HR:")
    for position in positions_active_or_hr:
        print(position.title)

    print("Запит 4 - Назви відділів з менеджерами:")
    for department in departments_with_managers_names:
        print(department['name'])

    print("Запит 5 - Позиції, відсортовані за назвою та інформацією про активність:")
    for position in positions_sorted:
        print(f"Назва: {position['title']}, Активність: {position['is_active']}")

    # Повертаємо пустий відгук, так як весь вивід відбувається в консоль
    return render(request, 'empty_template.html')


def user_is_superadmin(user) -> bool:
    return user.is_superuser


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(position__title__icontains=search),
                Q(email__icontains=search),
            )
        return queryset


class NewEmployeeListView(DetailView):
    model = Employee
    template_name = 'new_employee_list.html'
    context_object_name = 'employee'
    paginate_by = 10

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
