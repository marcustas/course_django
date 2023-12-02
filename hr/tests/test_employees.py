from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
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


class EmployeeListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employees_count = 10
        self.employees = EmployeeFactory.create_batch(self.employees_count)
        self.client.force_login(user=self.employees[0])
        self.url = reverse('hr:employee_list')

    def test_access_employee_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_employee_list_content(self):
        response = self.client.get(self.url)
        self.assertTrue('employees' in response.context)
        self.assertEqual(len(response.context['employees']), self.employees_count)

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


class EmployeeProfileView(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.employee = EmployeeFactory()
        self.url = reverse('hr:employee_profile', args=(self.employee.pk,))

    def test_access_employee_profile_view(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class EmployeeDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.employee = EmployeeFactory()
        self.url = reverse('hr:employee_delete', args=(self.employee.pk,))

    def test_employee_delete(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):  # можно было бы так проверить, если бы использовался Employee() ??
            Employee.objects.get(id=self.employee.pk)


class EmployeeUpdateView(TestCase):
    def setUp(self):
        self.employee = EmployeeFactory()
        self.url = reverse('hr:employee_update', args=(self.employee.pk,))
        self.updated_data = {
            'first_name': 'Bob',
            'last_name': 'McShnackneks',
        }
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.non_admin_user = EmployeeFactory(is_staff=False, is_superuser=False)

    def test_employee_update_as_admin(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(self.url, self.updated_data)
        self.assertEqual(response.status_code, 200)

    def test_employee_update_as_simple_user(self):
        self.client.force_login(self.non_admin_user)
        response = self.client.post(self.url, self.updated_data)
        self.assertEqual(response.status_code, 403)