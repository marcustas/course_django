from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse

from hr.forms import EmployeeForm
from hr.models import Employee, Department, Position


def user_is_superadmin(user) -> bool:
    return user.is_superuser


@user_passes_test(user_is_superadmin)
def employee_list(request):
    search = request.GET.get('search', '')
    employees = Employee.objects.all()

    if search:
        employees = employees.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(position__title__icontains=search),
        )

    for employee in employees:
        print(employee.birth_date)

    context = {'employees': employees}
    return render(request, 'employee_list.html', context)


@user_passes_test(user_is_superadmin)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('employee_list'))
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})


@user_passes_test(user_is_superadmin)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect(reverse('employee_list'))
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})


@user_passes_test(user_is_superadmin)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect(reverse('employee_list'))
    return render(request, 'employee_confirm_delete.html', {'object': employee})


@user_passes_test(user_is_superadmin)
def homework_querysets(request):
    all_departments_with_managers = Department.objects.filter(position__is_manager=True).order_by('name')
    count_active_positions = Position.objects.filter(is_active=True).count()
    active_or_hr_positions = Position.objects.filter(department__name='HR') | Position.objects.filter(is_active=True)
    departments_with_managers = Department.objects.filter(position__is_manager=True).values('name')
    positions_sorted_by_name = Position.objects.all().order_by('title').values('title', 'is_manager')

    context = {
        'all_departments_with_managers': all_departments_with_managers,
        'count_active_positions': count_active_positions,
        'active_or_hr_positions': active_or_hr_positions,
        'departments_with_managers': departments_with_managers,
        'positions_sorted_by_name': positions_sorted_by_name,
    }

    return render(request, 'homework_querysets.html', context)
