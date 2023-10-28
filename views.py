# Create your views here.

from django.views.generic import DetailView
from .models import Employee


class EmployeeProfileView(DetailView):
    model = Employee
    template_name = 'employee_profile.html'
    context_object_name = 'employee'

