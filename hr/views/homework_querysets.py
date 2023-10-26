from django.views.generic import ListView
from hr.models import Department, Position
from django.db.models import Count, Q
from django.http import JsonResponse

class HomeworkQuerysetsView(ListView):
    def get(self, request, *args, **kwargs):

        departments_with_managers = Department.objects.filter(position__is_manager=True).order_by('name')
        total_active_positions = Position.objects.filter(is_active=True).count()
        active_positions_or_hr = Position.objects.filter(Q(is_active=True) | Q(department__name="HR"))
        departments_with_managers_names = Department.objects.filter(position__is_manager=True).values('name')
        sorted_positions = Position.objects.filter(is_active=True).order_by('title').values('title', 'is_active')

        response_data = {
            'departments_with_managers': list(departments_with_managers.values()),
            'total_active_positions': total_active_positions,
            'active_positions_or_hr': list(active_positions_or_hr.values()),
            'departments_with_managers_names': list(departments_with_managers_names),
            'sorted_positions': list(sorted_positions),
        }

        return JsonResponse(response_data)
