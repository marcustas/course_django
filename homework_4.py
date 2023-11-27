from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin
from django.core.exceptions import ValidationError


class Company(models.Model):
    name = models.CharField
    address = models.CharField
    email = models.EmailField
    tax_code = models.CharField

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and Company.objects.exists():
            raise ValidationError('There can be only one Company instance.')
        return super(Company, self).save(*args, **kwargs)


class Position(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    job_description = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        if self.is_manager:
            existing_manager = Position.objects.filter(department=self.department, is_manager=True).exists()
            if existing_manager:
                raise ValidationError(f'Manager already exists in the {self.department.name} department.')
        super(Position, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Employee(AbstractUser):
    hire_date = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'position', 'hire_date', 'phone_number')
