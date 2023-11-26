from django.db.models import (
    Count,
    Q,
)
from django.http import HttpResponse
from hr.models import (
    Department,
    Position,
)


def querysets_examples(request):
    all_active_positions = Position.objects.filter(is_active=True)

    explain = all_active_positions.explain()
    sql_query = str(all_active_positions.query)

    non_manager_positions = Position.objects.exclude(is_manager=True)

    departments_with_positions_count = Department.objects.annotate(num_positions=Count('position'))

    total_active_positions = Position.objects.filter(is_active=True).aggregate(num_active=Count('id'))

    positions_by_title = Position.objects.order_by('title')

    distinct_departments = Department.objects.values('name').distinct()

    values = Position.objects.values('title', 'is_manager')
    values_list = Position.objects.values_list('title', 'is_manager')

    extra_positions = Position.objects.extra(select={'is_new': 'is_manager = False AND is_active = True'})
    is_new = extra_positions[0].is_new

    deferred = Position.objects.defer('job_description')
    only_title = Position.objects.only('title')

    # OR (|)
    and_positions = Position.objects.filter(Q(is_active=True) | Q(is_manager=False))
    and_positions = Position.objects.filter(is_active=True, is_manager=False)
    or_positions = Position.objects.filter(is_active=True) | Position.objects.filter(is_manager=False)

    # non-queryset methods
    first_position = Position.objects.first()
    get_position = Position.objects.get(id=first_position.id)

    created = Department.objects.create(
        name='New Departmnet',
    )

    department, created = Department.objects.get_or_create(name='HR')

    count_positions = Position.objects.count()

    last_position = Position.objects.last()

    exists_positions = Position.objects.filter(is_active=False).exists()

    # Deleted positions where is_manager is True
    deleted, _rows_count = Position.objects.filter(is_manager=False).delete()

    for position in Position.objects.iterator(chunk_size=1000):
        print(position.title)
    Position.objects.iterator()
    # Lookups
    department = Department.objects.first()
    positions_starting_with_d = Position.objects.filter(title__startswith='D')
    positions_containing_manager = Position.objects.filter(title__icontains='teac')
    positions_in_date_range = Position.objects.filter(department__name__range=('A', 'Z'))

    # JOINs в Django (INNER JOIN приклад)
    inner_joined = Position.objects.select_related('department')


    # JOINs в Django (LEFT OUTER JOIN приклад)
    left_joined = Department.objects.prefetch_related('positions').distinct()

    return HttpResponse()
