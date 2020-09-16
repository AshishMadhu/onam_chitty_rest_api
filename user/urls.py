from django.urls import path
from . import api_view

app_name = 'user'

urlpatterns = [
    path('api/signup/', api_view.RegisterAPI.as_view(), name = 'signup'),
    path('api/login/', api_view.LoginAPI.as_view(), name = 'login'),
]