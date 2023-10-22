from django.db import models
from django.core.exceptions import ValidationError

class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    tax_code = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Забезпечення того, що існує лише один інстанс
        if Company.objects.exists() and not self.pk:
            raise ValidationError('There can be only one Company instance.')
        return super(Company, self).save(*args, **kwargs)


class Employee(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=13)


class Position(models.Model):
    job_description = models.CharField(max_lenght=100)

