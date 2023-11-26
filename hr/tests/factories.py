import factory
from django.contrib.auth.hashers import make_password

from hr.models import (
    Department,
    Employee,
    Position,
)


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    name = factory.Faker('word')


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position

    title = factory.Faker('job')
    department = factory.SubFactory(DepartmentFactory)


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    username = factory.Sequence(lambda n: f'user{n}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = make_password('password')
