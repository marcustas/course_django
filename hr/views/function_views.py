from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, QuerySet
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse

from hr.forms import EmployeeForm
from hr.models import Employee, Position, Department


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


def homework_querysets(request):
    # department_names = Department.objects.values_list('name', flat=True)
    # for name in department_names:
        # if a := Department.objects.get(name=name).position_set.filter(is_manager=True):
        #     a.order_by('departmnet')

    template_name = 'homework_querysets.html'

    query_1 = Department.objects.filter(position__is_manager=True).order_by('department')
    query_2 = Position.objects.filter(is_active=True).count()
    query_3 = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))
    query_4 = Department.objects.filter(position__is_manager=True).values('name')
    query_5 = Position.objects.order_by('title').values('title', 'job_description')

    context = {
        'query_1': query_1,
        'query_2': query_2,
        'query_3': query_3,
        'query_4': query_4,
        'query_5': query_5,
    }
    return render(request, template_name, context=context)


def training(request):
    return render(request, 'training.html')