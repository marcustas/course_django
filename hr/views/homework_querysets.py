from hr.models import Department, Position
from django.shortcuts import render
from django.db.models import Count, Q


def query_sets(request):
    department_with_manager = Department.objects.filter(position__is_manager=True).order_by('name')
    count_of_active_position = Position.objects.filter(is_active=True).count()
    activ_posistion_or_HR = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))
    departments_with_managers_names = Department.objects.filter(position__is_manager=True).values('name')
    position_sorted_by_name = Position.objects.filter(is_active=True).order_by('title').values('title', 'is_active')

    context={
        'department_with_manager' : department_with_manager,
        'count_of_active_position' : count_of_active_position,
        'activ_posistion_or_HR' : activ_posistion_or_HR,
        'departments_with_managers_names' : departments_with_managers_names,
        'position_sorted_by_name' : position_sorted_by_name,
    }
    return render (request,'homework_query_sets.html',context)