import pytz
from unittest import mock
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.test import APITestCase
from onam_chitty.factories import ChittyFactory, MemberFactory
from . mixins import BasicMixin

class TestMemberViewSet(BasicMixin, APITestCase):

    assertion_error = 'Pass chitty_id in url'
    url_prefix = 'onam_chitty:api:member'

    def test_list_view(self):
        chitty = ChittyFactory()
        for i in range(20):
            MemberFactory(chitty = chitty)
        url = self.get_url('list', chitty_id = chitty.id)
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

        # with invalid chitty_id 
        url = self.get_url('list', chitty_id = 23)
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # without chitty_id
        url = url.split('?')[0]
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_view(self):
        """ 
        * True case 
            # check chitty is added 
            # check id is created
        * empty data
        * with different owner
        * invalid chitty_id
        * without chitty_id
        * without authorization
         """
        user, _ = self.create_user_set_authentication_credentials()
        chitty = ChittyFactory(owner = user)
        url = self.get_url('list', chitty_id = chitty.id)
        data = {
            'name': 'kannan',
        }
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['chitty'], 1)
        self.assertIsNotNone(response.data['id'])
        data = {}

        # empty data
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # with different owner
        chitty2 = ChittyFactory()
        url = url.split('=')[0] + f'={chitty2.id}'
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], self.forbidden)

        # invalid chitty_id
        url = url.split('=')[0] + '=75'
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], self.forbidden)

        # without chitty_id
        url = url.split('?')[0]
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], self.assertion_error)
    
    def test_retrieve_view(self):
        member = MemberFactory()
        url = self.get_url('detail', kwargs = {'pk': member.id})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # invalid pk
        url = self.get_url('detail', kwargs = {'pk': 10})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_delete_methods(self):
        time_out_error = "You cannot change the price after 5 min."
        member1 = MemberFactory()
        url = self.get_url('detail', kwargs = {'pk': member1.id})
        data = {
            'name': 'susilan'
        }
        # without authorization
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # testing PATCH, PUT, after 5 min
        user, _ = self.create_user_set_authentication_credentials()
        chitty = ChittyFactory(owner = user)
        member = MemberFactory(chitty = chitty)
        mocked = (datetime.utcnow() + timedelta(minutes = 5)).replace(tzinfo = pytz.utc)
        url = self.get_url('detail', kwargs = {'pk': member.id})
        with mock.patch('onam_chitty.models.Member.get_now', mock.Mock(return_value = mocked)):
            patch_response = self.client.patch(url, data, format = 'json')
            put_response = self.client.put(url, data, format = 'json')
            self.assertEqual(patch_response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(patch_response.data['detail'], time_out_error)
            self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(put_response.data['detail'], time_out_error)
        
        # All ture case PATCH
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

        # PATCH with member of other chitty
        _url = self.get_url('detail', kwargs = {'pk': member1.id})
        response = self.client.patch(_url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], self.forbidden)

        # All ture case PUT
        response = self.client.put(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

        # DELETE request
        response = self.client.delete(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

