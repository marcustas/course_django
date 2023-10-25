from django.db.models import Count
from django.http import HttpResponse

from hr.models import Department, Position


def querysets_examples(request):
    # Retrieve all active positions
    all_active_positions = Position.objects.filter(is_active=True)

    # Explain the query execution plan
    explain = all_active_positions.explain()

    # Get the SQL query string
    sql_query = str(all_active_positions.query)

    # Retrieve non-manager positions
    non_manager_positions = Position.objects.exclude(is_manager=True)

    # Count the number of positions for each department
    departments_with_positions_count = Department.objects.annotate(num_positions=Count('position'))

    # Count the total number of active positions
    total_active_positions = Position.objects.filter(is_active=True).aggregate(num_active=Count('id'))

    # Retrieve positions ordered by title
    positions_by_title = Position.objects.order_by('title')

    # Retrieve distinct department names
    distinct_departments = Department.objects.values('name').distinct()

    # Retrieve position titles and is_manager values
    values = Position.objects.values('title', 'is_manager')

    # Retrieve position titles and is_manager values as a list
    values_list = Position.objects.values_list('title', 'is_manager')

    # Retrieve extra positions with an "is_new" attribute
    extra_positions = Position.objects.extra(select={'is_new': 'is_manager = False AND is_active = True'})
    is_new = extra_positions[0].is_new

    # Retrieve positions with deferred "job_description" field
    deferred = Position.objects.defer('job_description')

    # Retrieve positions with only the "title" field
    only_title = Position.objects.only('title')

    # Retrieve active non-manager positions
    and_positions = Position.objects.filter(is_active=True, is_manager=False)

    # Retrieve active non-manager positions (alternative syntax)
    and_positions = Position.objects.filter(is_active=True).filter(is_manager=False)

    # Retrieve active positions or non-manager positions
    or_positions = Position.objects.filter(is_active=True) | Position.objects.filter(is_manager=False)

    # Retrieve the first position
    first_position = Position.objects.first()

    # Retrieve a position by ID
    get_position = Position.objects.get(id=first_position.id)

    # Create a new department
    created = Department.objects.create(name='New Department')

    # Get or create a department with name "HR"
    department, created = Department.objects.get_or_create(name='HR')

    # Count the number of positions
    count_positions = Position.objects.count()

    # Retrieve the last position
    last_position = Position.objects.last()

    # Check if there are inactive positions
    exists_positions = Position.objects.filter(is_active=False).exists()

    # Delete non-manager positions and get the number of deleted rows
    deleted, _rows_count = Position.objects.filter(is_manager=False).delete()

    # Iterate over positions
    Position.objects.iterator()

    # Retrieve the first department
    department = Department.objects.first()

    # Retrieve positions with titles starting with 'D'
    positions_starting_with_d = Position.objects.filter(title__startswith='D')

    # Retrieve positions with titles containing 'teac'
    positions_containing_manager = Position.objects.filter(title__icontains='teac')

    # Retrieve positions in a specific date range
    positions_in_date_range = Position.objects.filter(department__name__range=('A', 'Z'))

    # Retrieve positions with department information using inner join
    inner_joined = Position.objects.select_related('department')

    # Retrieve departments with positions using left join and prefetch_related
    left_joined = Department.objects.prefetch_related('positions').distinct()

    return HttpResponse()
