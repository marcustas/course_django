from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from phone_field import PhoneField


class Department(models.Model):
    name = models.CharField(max_length=200)
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    job_description = models.CharField(max_length=200, blank=True)

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
    phone_number = PhoneField(help_text='Phone number', blank=True)


class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    tax_number = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.pk and Company.objects.exists():
            raise ValidationError(f'Company with name {self.name} already exists.')
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
