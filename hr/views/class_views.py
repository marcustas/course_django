from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse
from django.views import View

from hr.forms import EmployeeForm
from hr.models import Employee, Department, Position


def user_is_superadmin(user) -> bool:
    return user.is_superuser


class EmployeeListView(View):
    def get(self, request):
        search = request.GET.get('search', '')
        employees = Employee.objects.all()

        if search:
            employees = employees.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(position__title__icontains=search)
                | Q(email__icontains=search),
            )

        # Debugging: Print the search string and filtered employees
        print(f"Search String: {search}")
        print("Filtered Employees:")
        for emp in employees:
            print(emp.email)  # Print emails for debugging

        # Print the SQL query
        print(employees.query)

        context = {'employees': employees}
        return render(request, 'employee_list.html', context)


class EmployeeCreateView(UserPassesTestMixin, View):
    def get(self, request):
        form = EmployeeForm()
        return render(request, 'employee_form.html', {'form': form})

    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('employee_list'))
        return render(request, 'employee_form.html', {'form': form})

    def test_func(self):
        return user_is_superadmin(self.request.user)


class EmployeeUpdateView(UserPassesTestMixin, View):
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeForm(instance=employee)
        return render(request, 'employee_form.html', {'form': form})

    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect(reverse('employee_list'))
        return render(request, 'employee_form.html', {'form': form})

    def test_func(self):
        return user_is_superadmin(self.request.user)


class EmployeeDeleteView(UserPassesTestMixin, View):
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        return render(
            request, 'employee_confirm_delete.html', {'object': employee}
        )

    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return redirect(reverse('employee_list'))

    def test_func(self):
        return user_is_superadmin(self.request.user)


class InfoFromDb(View):
    def get(self, request, *args, **kwargs):
        departments_with_managers_query = Department.objects.filter(
            position__is_manager=True)

        departments_with_managers_names = list(
            departments_with_managers_query.values_list('name', flat=True))

        ordered_departments_with_managers = list(
            departments_with_managers_query.order_by('department').values_list(
                'name', flat=True))

        active_positions_count = Position.objects.filter(is_active=True).count()

        positions_in_hr_or_active = list(
            Position.objects.filter(
                Q(department__name='HR') | Q(is_active=True)
            ).values_list('title', flat=True)
        )



        positions_sorted = Position.objects.order_by('title').values(
            'title', 'is_active'
        )

        data = {
            'ordered_departments_with_managers': ', '.join(ordered_departments_with_managers),
            'active_positions_count': str(active_positions_count),
            'positions_in_hr_or_active': ', '.join(
                positions_in_hr_or_active
            ),
            'departments_with_managers_names': ', '.join(
                departments_with_managers_names
            ),
            'positions_sorted': list(positions_sorted),
        }

        return render(request, 'info_from_db.html', data)
