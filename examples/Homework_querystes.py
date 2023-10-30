from django.db.models import (
    Count,
    Q,
)

from django.shortcuts import render

from hr.models import (
    Department,
    Position,
)

def homework_querysets(request):

    department_is_manager = Department.objects.filter(position__is_manager=True).order_by('name')

    count_is_active = Position.objects.filter(is_active=True).count()

    position_or = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))

    department_name = Department.objects.filter(position__is_manager=True).values('name')

    position_is_active = Position.objects.order_by('-title').values('title', 'is_active')


    department_list = [department.name for department in department_is_manager]
    count_list = [count_is_active]
    position_list = [position.title for position in position_or]
    department_name_list = [name for name in department_name]
    position_is_active_list = [position for position in position_is_active]


    # Об'єднайте обидва списки в один
    results_list = department_list + count_list + position_list + department_name_list + position_is_active_list

    context = {
        'results': results_list
    }

    return render(request, 'Homework.html', context)