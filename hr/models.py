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
    job_description = models.CharField(max_length=200,)

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
    phone_number = models.CharField(max_length=20)


class Company(models.Model):
    name_company = models.CharField(max_length=30)
    adress_company = models.CharField(max_length=40)
    email_company = models.EmailField(max_length=50)
    tax_code = models.CharField(max_length=30)

    def save(self,*args, **kwargs):
        if not self.pk and Company.object.exist():
            raise ValidationError('There can be only one Company instance.')
        return super(Company, self).save(*args,**kwargs)

    def __str__(self):
        return self.tittle





