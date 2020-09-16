import pytz
from unittest import mock
from datetime import datetime, timedelta
from django.db.models import Sum
from rest_framework import status
from rest_framework.test import APITestCase
from onam_chitty.models import Log
from onam_chitty.factories import ChittyFactory, LogFactory, MemberFactory
from user.factories import UserFactory
from . mixins import BasicMixin

class TestLogViews(BasicMixin, APITestCase):
    url_prefix = 'onam_chitty:api:log'
    member_id_assertion_error = 'Pass member_id in url'

    def test_list_view(self):
        utc = pytz.timezone('utc')
        chitty = ChittyFactory()
        member = MemberFactory(chitty = chitty)
        for i in range(10):
            LogFactory(member = member)
        for i in range(5):
            LogFactory(member = member, date = datetime(2020, 9, 2).replace(tzinfo = utc))
        LogFactory()
        url = self.get_url('list', member_id = member.id)
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 15)
        self.assertEqual(len(response.data['results']['results']), 10)
        self.assertIn('total', response.data['results'])

        # without member_id
        url = url.split('?')[0]
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], self.member_id_assertion_error)

    def test_create_view(self):
        """ 
        * Without authentication
        * All valid case
        * Price > 10000 & < 10
        * With member of other chitty
        """

        # without authentication
        user = UserFactory()
        chitty = ChittyFactory(owner = user)
        member = MemberFactory(chitty = chitty)
        url = self.get_url('list', member_id = member.id)
        data = {
            'price_given': 45,
        }
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # authenticating user
        self.create_user_set_authentication_credentials(user = user)

        # All valid case
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # price > 10000 & < 10
        data.update({
            'price_given': 100005,
        })
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['price_given'][0], 'Ensure this value is less than or equal to 10000.')

        data.update({
            'price_given': 5
        })
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['price_given'][0], 'Ensure this value is greater than or equal to 10.')

        member2 = MemberFactory()
        url = self.get_url('list', member_id = member2.id)
        data.update({
            'price_given': 45,
        })
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.data['detail'], self.forbidden)

    def test_update_view(self):
        """ 
        * Unauthenticated
        * with a log having member of other chitty
        * time greater than 4 minutes
        * all valid case
        * test the PUT
         """

        # Unauthenticated
        log1 = LogFactory()
        url = self.get_url('detail', kwargs = {'pk': log1.pk})
        response = self.client.patch(url, {}, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Log having member of other chitty
        user, _ = self.create_user_set_authentication_credentials()
        url = self.get_url('detail', kwargs = {'pk': log1.pk})
        response = self.client.patch(url, {}, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Time greater than 4 min
        chitty = ChittyFactory(owner = user)
        member = MemberFactory(chitty = chitty)
        log = LogFactory(member = member)
        mocked = (datetime.utcnow() + timedelta(minutes = 5)).replace(tzinfo = pytz.utc)
        url = self.get_url('detail', kwargs = {'pk': log.pk})
        time_exceed_error = "You cannot change the price after 5 min."
        data = {
            'price_given': 13,
        }
        with mock.patch('onam_chitty.models.Log.get_now', mock.Mock(return_value = mocked)):
            response = self.client.patch(url, data, format = 'json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(response.data['detail'], time_exceed_error)
        
        # all valid case
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price_given'], data['price_given'])

        # Test PUT
        log2 = LogFactory(member = member)
        url = self.get_url('detail', kwargs = {'pk': log2.id})
        response = self.client.put(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price_given'], data['price_given'])
