from django.urls import path

from hr.views import generic_views as views
from hr.views import function_views as func_views


urlpatterns = [
    path('employees/queries/', func_views.homework_querysets, name='homework_querysets'),
    path('employees/details/<int:pk>/', views.EmployeeProfileView.as_view(), name='employee_view'),
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/update/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/delete/<int:pk>/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employees/profile/<int:pk>/', views.EmployeeProfileView.as_view(), name='employee_profile'),
    path('salary-calculator/', views.SalaryCalculatorView.as_view(), name='salary_calculator'),
]
