from django.urls import path, include
from django.views.decorators.cache import cache_page

from hr import views
from rest_framework.routers import DefaultRouter
from hr.views import DepartmentViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    path('api/', include(router.urls)),
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/update/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/delete/<int:pk>/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employees/profile/<int:pk>/', cache_page(60*1)(views.EmployeeProfileView.as_view()), name='employee_profile'),
    path('salary-calculator/', views.SalaryCalculatorView.as_view(), name='salary_calculator'),
]
