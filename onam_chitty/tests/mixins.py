from django.urls import reverse
from django.utils.http import urlencode
from knox.auth import AuthToken
from user.factories import UserFactory

class BasicMixin(object):
    url_prefix = None
    
    # error messages
    forbidden = 'You do not have permission to perform this action.'
    
    def print_r(self, response):
        print(response)
        print(response.data)

    def get_url(self, *args, **kwargs):
        assert self.url_prefix, 'You need to set the url prefix'
        url_kwargs = None
        if 'kwargs' in kwargs:
            url_kwargs = kwargs.pop('kwargs')
        url = reverse(f'{self.url_prefix}-{args[0]}', kwargs = url_kwargs)
        url += f'?{urlencode(kwargs)}'
        return url
    
    def create_user_set_authentication_credentials(self, user = None):
        if user == None:
            user = UserFactory()
        _, token = AuthToken.objects.create(user = user)
        self.client.credentials(
            HTTP_AUTHORIZATION = 'Token {0}'.format(token)
        )
        return user, token