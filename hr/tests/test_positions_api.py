from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from hr.models import Position, Employee
from hr.tests.factories import PositionFactory


class PositionViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Employee.objects.create_user(username='testuser',
                                                 password='testpassword',
                                                 email='test@gmail.com')
        self.position = PositionFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_position_list(self):
        response = self.client.get(reverse('api-hr:position-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_position(self):
        data = {
            'title': 'New Position',
            'department': '1',
        }
        response = self.client.post(reverse('api-hr:position-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_position(self):
        position = PositionFactory()
        data = {'title': 'Updated Position'}
        response = self.client.patch(reverse('api-hr:position-detail',
                                             kwargs={'pk': position.pk}),
                                     data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_position(self):
        position = PositionFactory()
        response = self.client.delete(reverse('api-hr:position-detail',
                                              kwargs={'pk': position.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
