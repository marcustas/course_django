from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=200)
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    job_description = models.TextField(blank=True, null=True)

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
    phone_number = models.CharField(max_length=20, blank=True, null=True)


class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    tax_code = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        if Company.objects.exists() and not self.pk:
            raise ValidationError('There can be only one Company instance.')
        return super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
