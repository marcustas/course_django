from django.urls import path

from hr.views import generic_views as views
from hr.views.function_views import homework_querysets


urlpatterns = [
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/update/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/delete/<int:pk>/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employees/profile/<int:pk>/', views.EmployeeProfileView.as_view(), name='employee_profile'),
    path('homework_querysets/', homework_querysets, name='homework_querysets'),
]
