from django.contrib import admin
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname','phone_number')

admin.site.register(Employee, EmployeeAdmin)
