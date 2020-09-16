from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from knox.auth import AuthToken
from user.factories import UserFactory

class TestUserAction(APITestCase):
    def test_register_api(self):
        data = {
            'username': 'atom',
            'password': 'TestPass@123',
            'email': 'atom@hiestAsh.com'
        }
        url = reverse('user:signup')
        response = self.client.post(url, data, format = 'json')
        token = response.data['token']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token_key = AuthToken.objects.all().get().token_key
        self.assertTrue(token_key == token[:8])
 
    def test_login_api(self):
        user = UserFactory()
        url = reverse('user:login')
        data = {
            'username': user.username,
            'password': 'TestPass@123'
        }
        response = self.client.post(url, data, format = 'json')
        token = response.data['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token_key = AuthToken.objects.all().get().token_key
        self.assertTrue(token_key == token[:8])
        self.assertTrue(response.data['user']['id'] == user.id)
        # test with a wrong password
        data.update({
            'password': 'Testpass@123'
        })
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)