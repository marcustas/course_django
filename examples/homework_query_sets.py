from hr.models import Department, Position
from django.shortcuts import render


def homework_query_sets(request):
    departments_with_managers = Department.objects.filter(position__is_manager=True).order_by('name')
    active_positions_count = Position.objects.filter(is_active=True).count()
    active_positions_in_hr = Position.objects.filter(is_active=True) | Position.objects.filter(department__name='HR')
    departments_with_managers_names = Department.objects.filter(position__is_manager=True).values('name')
    positions_sorted_by_name = Position.objects.order_by('name').values('name', 'is_active')

    context = {
        'departments_with_managers': departments_with_managers,
        'active_positions_count': active_positions_count,
        'active_positions_in_hr': active_positions_in_hr,
        'departments_with_managers_names': departments_with_managers_names,
        'positions_sorted_by_name': positions_sorted_by_name,
    }

    return render(request, 'homework_query_sets.html', context)
