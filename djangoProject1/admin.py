@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'position', 'hire_date')
    list_display = ('username', 'position', 'hire_date', 'phone_number')