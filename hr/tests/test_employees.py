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

    #2
    class EmployeeProfileViewTest(TestCase):
        def setUp(self):
            self.client = Client()
            self.employee = EmployeeFactory()
            self.url = reverse('hr:employee_profile', args=[self.employee.id])

        def test_access_employee_profile(self):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)


    class EmployeeDeleteViewTest(TestCase):
        def setUp(self):
            self.client = Client()
            self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
            self.employee_to_delete = EmployeeFactory()
            self.url = reverse('hr:employee_delete', args=[self.employee_to_delete.id])

        def test_delete_employee_by_admin(self):
            self.client.force_login(self.admin_user)
            response = self.client.post(self.url)
            self.assertEqual(response.status_code, 302)
            self.assertFalse(Employee.objects.filter(id=self.employee_to_delete.id).exists())


    class EmployeeUpdateViewTest(TestCase):
        def setUp(self):
            self.client = Client()
            self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
            self.employee_to_update = EmployeeFactory()
            self.new_position = PositionFactory()
            self.url = reverse('hr:employee_update', args=[self.employee_to_update.id])

        def test_update_employee_by_admin(self):
            self.client.force_login(self.admin_user)
            new_first_name = 'UpdatedFirstName'
            new_last_name = 'UpdatedLastName'
            new_email = 'updated@example.com'
            new_position_id = self.new_position.id
            updated_data = {
                'first_name': new_first_name,
                'last_name': new_last_name,
                'email': new_email,
                'position': new_position_id,
            }
            response = self.client.post(self.url, updated_data)
            self.assertEqual(response.status_code, 302)

            updated_employee = Employee.objects.get(id=self.employee_to_update.id)
            self.assertEqual(updated_employee.first_name, new_first_name)
            self.assertEqual(updated_employee.last_name, new_last_name)
            self.assertEqual(updated_employee.email, new_email)
            self.assertEqual(updated_employee.position.id, new_position_id)
