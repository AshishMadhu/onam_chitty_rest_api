from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APITestCase
from knox.auth import AuthToken
from user.factories import UserFactory
from onam_chitty.factories import ChittyFactory

class TestChittyViewSet(APITestCase):

    def create_user_set_authentication_credentials(self):
        user = UserFactory()
        _, token = AuthToken.objects.create(user = user)
        self.client.credentials(
            HTTP_AUTHORIZATION = 'Token {0}'.format(token)
        )
        return user, token
    
    def get_url(self, *args, **kwargs):
        url_kwargs = None
        if 'kwargs' in kwargs:
            url_kwargs = kwargs.pop('kwargs')
        url = reverse(f'onam_chitty:api:chitty-{args[0]}', kwargs = url_kwargs)
        url += f'?{urlencode(kwargs)}'
        return url

    def test_create_view(self):
        user, _ = self.create_user_set_authentication_credentials()
        url = self.get_url('list')
        data = {
            'type': 'on',
        }
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # without user
        self.client.credentials()
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_retrieve_view(self):
        user, _ = self.create_user_set_authentication_credentials()
        chitty = ChittyFactory(owner = user,)
        url = self.get_url('detail', kwargs = {'pk': chitty.id})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], chitty.id)

        # withinvalid id
        url = self.get_url('detail', kwargs = {'pk': 23})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # without user
        self.client.credentials()
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
