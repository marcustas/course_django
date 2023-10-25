from django.db.models import Q
from django.http import JsonResponse

from hr.models import Department, Position


#ruff: noqa: E501
def hw_querysets(request):
    """
        Retrieves various querysets and returns a JsonResponse with the results.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response containing the following data:
                - departments_with_managers (list): A list of dictionaries representing departments with managers.
                - count_of_active_positions (int): The count of active positions.
                - active_or_hr_positions (list): A list of dictionaries representing active or HR positions.
                - name_of_departments_managers (list): A list of dictionaries representing the names of department managers.
                - sorted_positions (list): A list of dictionaries representing sorted positions.

    """
    departments_with_managers = Department.objects.filter(position__is_manager=True).order_by('name')
    count_of_active_positions = Position.objects.filter(is_active=True).count()
    active_or_hr_positions = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))
    name_of_departments_managers = Department.objects.filter(position__is_manager=True).values('name')
    sorted_positions = Position.objects.values('title', 'is_active').order_by('title')

    response = {
        'departments_with_managers': list(departments_with_managers.values()),
        'count_of_active_positions': count_of_active_positions,
        'active_or_hr_positions': list(active_or_hr_positions.values()),
        'name_of_departments_managers': list(name_of_departments_managers),
        'sorted_positions': list(sorted_positions),
    }

    return JsonResponse(response)
