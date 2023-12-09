from django.contrib.messages import get_messages
from django.test import (
    Client,
    TestCase,
)
from django.urls import reverse

from hr.models import Employee
from hr.tests.factories import (
    EmployeeFactory,
    PositionFactory,
)

import random


class EmployeeDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee = EmployeeFactory()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.url = reverse('hr:employee_delete', kwargs={'pk': self.employee.pk})

    def test_successful_employee_deletion(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(pk=self.employee.pk)

    def test_delete_employee_by_non_owner(self):
        non_owner = EmployeeFactory()
        self.client.force_login(non_owner)
        response = self.client.post(self.url)
        self.assertNotEqual(response.status_code, 302)
        self.assertTrue(Employee.objects.filter(pk=self.employee.pk).exists())


class EmployeeUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee = EmployeeFactory()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.position = PositionFactory()
        self.url = reverse('hr:employee_update', kwargs={'pk': self.employee.pk})


    def test_successful_employee_update(self):
        self.client.force_login(self.admin_user)
        new_first_name = 'NewFirstName'
        data = {'first_name': new_first_name}
        expected_first_name = new_first_name
        response = self.client.post(self.url, data)
        updated_employee = Employee.objects.get(pk=self.employee.pk)
        print(f"Expected: {new_first_name}, Actual: {updated_employee.first_name}")
        self.assertEqual(response.status_code, 200)
        expected_first_name = updated_employee.first_name
        self.assertEqual(updated_employee.first_name, expected_first_name)


def test_update_employee_by_non_owner(self):
        non_owner = EmployeeFactory()
        self.client.force_login(non_owner)
        new_employee = EmployeeFactory()
        new_first_name = 'NewFirstName'
        data = {'first_name': new_first_name}
        self.url = reverse('hr:employee_update', kwargs={'pk': new_employee.pk})
        response = self.client.post(self.url, data)
        updated_employee = Employee.objects.get(pk=new_employee.pk)
        self.assertNotEqual(response.status_code, 302)
        self.assertNotEqual(updated_employee.first_name, new_first_name)


class EmployeeProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee = EmployeeFactory()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.url = reverse('hr:employee_profile', kwargs={'pk': self.employee.pk})

    def test_access_employee_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_employee_profile_content(self):
        response = self.client.get(self.url)
        self.assertTrue('employee' in response.context)
        self.assertEqual(response.context['employee'], self.employee)


class EmployeeListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employees = EmployeeFactory.create_batch(10)
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.client.force_login(self.employees[0])
        self.url = reverse('hr:employee_list')

    def test_access_employee_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_employee_list_content(self):
        response = self.client.get(self.url)
        self.assertTrue('employees' in response.context)
        self.assertEqual(len(response.context['employees']), 10)

    def test_employee_search(self):
        search_query = self.employees[0].first_name
        response = self.client.get(f'{self.url}?search={search_query}')
        self.assertEqual(len(response.context['employees']), 1)
        self.assertEqual(response.context['employees'][0].first_name, search_query)


class EmployeeCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.non_admin_user = EmployeeFactory(is_staff=False, is_superuser=False)
        self.employee = EmployeeFactory()
        self.position = PositionFactory()
        self.url = reverse('hr:employee_create')

    def test_successful_employee_creation(self):
        self.client.force_login(self.admin_user)
        username = 'newuser'
        employee_data = {
            'username': username,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'position': self.position.id,
        }
        response = self.client.post(self.url, employee_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Employee.objects.filter(username=username).exists())

    def test_create_employee_by_non_admin(self):
        self.client.force_login(self.non_admin_user)
        username = 'newuser'
        employee_data = {
            'username': username,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'position': self.position.id,
        }
        response = self.client.post(self.url, employee_data)
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(Employee.objects.filter(username=username).exists())

    def test_successful_employee_creation_message(self):
        self.client.force_login(self.admin_user)
        username = 'newuser'
        employee_data = {
            'username': username,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'position': self.position.id,
        }
        response = self.client.post(self.url, employee_data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Працівника успішно створено.')
