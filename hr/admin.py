from django.contrib import admin
from django.core.exceptions import ValidationError
from modeltranslation.admin import TranslationAdmin

from hr.models import (
    Department,
    Employee,
    MonthlySalary,
    Position,
    Company
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_department')


@admin.register(Position)
class PositionAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'department', 'is_manager')

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            form.add_error(None, e)
            super().save_model(request, obj, form, change)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'position', 'hire_date', 'phone_number')


@admin.register(MonthlySalary)
class MonthlySalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month_year', 'salary', 'paid')


@admin.register(Company)
class Company(admin.ModelAdmin):
    list_display = ('logo',)
