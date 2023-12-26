import json

from django.contrib.auth.decorators import user_passes_test
from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse

from hr.forms import EmployeeForm
from hr.models import Department, Position, Employee


def user_is_superadmin(user) -> bool:
    return user.is_superuser


@user_passes_test(user_is_superadmin)
def employee_list(request):
    search = request.GET.get("search", "")
    employees = Employee.objects.all()

    if search:
        employees = employees.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(position__title__icontains=search),
        )

    for employee in employees:
        print(employee.birth_date)

    context = {"employees": employees}
    return render(request, "employee_list.html", context)


@user_passes_test(user_is_superadmin)
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("employee_list"))
    else:
        form = EmployeeForm()
    return render(request, "employee_form.html", {"form": form})


@user_passes_test(user_is_superadmin)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect(reverse("employee_list"))
    else:
        form = EmployeeForm(instance=employee)
    return render(request, "employee_form.html", {"form": form})


@user_passes_test(user_is_superadmin)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        return redirect(reverse("employee_list"))
    return render(request, "employee_confirm_delete.html", {"object": employee})


def homework_querysets(request):
    response_dict = {
        # 1. Все Department, в которых есть позиция менеджер. Сортировка по названию департамента.
        "first_queryset": json.loads(
            serialize("json", Department.objects.filter(position__title__icontains="manager").order_by("name"))
        ),
        # 2. Общее количество активных позиций (Position).
        "second_queryset": Position.objects.filter(is_active=True).count(),
        # 3. Все позиции, которые активны, или принадлежат к департаменту 'HR'.
        "third_queryset": json.loads(
            serialize("json", Position.objects.filter(Q(is_active=True) | Q(department__name="HR")))
        ),
        # 4. Все департаменты в которых есть менеджеры. Использовать filter() и values().
        "fourth_queryset": list(Department.objects.filter(position__is_manager=True).values("name")),
        # 5. Все позиции отсортированные по названию, но выводить только title и is_active.
        "fifth_queryset": list(Position.objects.order_by("title").values("title", "is_active")),
    }

    return JsonResponse(response_dict, safe=False)
