from django.contrib.auth.models import User
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


class EmployeeListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employees = EmployeeFactory.create_batch(10)
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
        self.assertTrue(len(response.context['employees']), 1)
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


class EmployeeProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.employee = EmployeeFactory()
        self.url = reverse('hr:employee_profile', kwargs={'pk': self.employee.pk})

    def test_access_employee_profile_as_admin(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class EmployeeUpdateViewTest(TestCase):
    def setUp(self):
        self.employee = EmployeeFactory()
        self.update_url = reverse('hr:employee_update', kwargs={'pk': self.employee.pk})
        self.updated_data = {
            'first_name': 'Tyler',
        }

    def test_update_employee_without_permission(self):
        non_admin_user = EmployeeFactory(is_staff=False, is_superuser=False)
        self.client.force_login(non_admin_user)
        response = self.client.post(self.update_url, self.updated_data)
        self.assertEqual(response.status_code, 403)


class EmployeeDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.employee = EmployeeFactory()
        self.delete_url = reverse('hr:employee_delete', kwargs={'pk': self.employee.pk})

    def test_delete_employee(self):
        self.client.force_login(self.admin_user)
        initial_count = Employee.objects.count()
        response = self.client.post(self.delete_url)
        self.assertEqual(Employee.objects.count(), initial_count - 1)
        self.assertEqual(response.status_code, 302)


