from django.db.models import Q
from django.http import JsonResponse

from hr.models import Department, Position


#ruff: noqa: E501
def hw_querysets(request):
    """
    Retrieves various data from the database and constructs a response dictionary containing the following information:

    - `departments_with_managers`: A list of dictionaries representing departments with managers, ordered by name. Each dictionary contains the department's attributes.
    - `count_of_active_positions`: An integer representing the number of active positions in the database.
    - `active_or_hr_positions`: A list of dictionaries representing active positions or positions in the HR department. Each dictionary contains the position's attributes.
    - `name_of_departments_managers`: A list of dictionaries representing the names of departments with managers. Each dictionary contains the department's name attribute.
    - `sorted_positions`: A list of dictionaries representing the titles and active status of all positions, ordered by title. Each dictionary contains the position's title and is_active attributes.

    Parameters:
    - `request`: The HTTP request object.

    Returns:
    - A `JsonResponse` object containing the constructed response dictionary.
    """
    # Retrieve all departments with managers, ordered by name
    departments_with_managers = Department.objects.filter(position__is_manager=True).order_by('name')

    # Count the number of active positions
    count_of_active_positions = Position.objects.filter(is_active=True).count()

    # Retrieve all active positions or positions in the HR department
    active_or_hr_positions = Position.objects.filter(Q(is_active=True) | Q(department__name='HR'))

    # Retrieve the names of departments with managers
    name_of_departments_managers = Department.objects.filter(position__is_manager=True).values('name')

    # Retrieve the titles and active status of all positions, ordered by title
    sorted_positions = Position.objects.values('title', 'is_active').order_by('title')

    # Construct the response dictionary
    response = {
        'departments_with_managers': list(departments_with_managers.values()),
        'count_of_active_positions': count_of_active_positions,
        'active_or_hr_positions': list(active_or_hr_positions.values()),
        'name_of_departments_managers': list(name_of_departments_managers),
        'sorted_positions': list(sorted_positions),
    }

    # Return the response as a JSON object
    return JsonResponse(response)
