from django.urls import (
    include,
    path,
)
from rest_framework.routers import DefaultRouter

from hr.api_views import (
    EmployeeViewSet,
    PositionViewSet,
    SalaryCalculatorView,
    DepartmentViewSet,
)


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'positions', PositionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('calculate_salary/', SalaryCalculatorView.as_view(), name='calculate_salary'),
]

