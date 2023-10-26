from django.http import HttpResponse
from hr.models import (
    Department,
    Position,
)


def homework_querysets(request):
    managers_by_department = Department.objects.filter(position__is_manager=True).order_by('name')

    active_position = Position.objects.filter(is_active=True).count()

    position_active_or_hr = Position.objects.filter(is_active=True) | Position.objects.filter(department__name='hr')

    department_with_managers = Department.objects.filter(position__is_manager=True).values('name')

    position_sorted = Position.objects.order_by('title').values('title', 'is_active')

    print(managers_by_department)
    print(active_position)
    print(position_active_or_hr)
    print(department_with_managers)
    print(position_sorted)

    return HttpResponse()
