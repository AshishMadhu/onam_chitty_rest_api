from django.contrib.auth.signals import user_logged_in
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from . import serializers

# user actions 
class RegisterAPI(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request, format = None, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            'user': serializer.data,
            'token': token
            }, status = status.HTTP_201_CREATED
        )

class LoginAPI(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        request.user = user
        user_logged_in.send(sender=request.user.__class__, request=request, user=request.user)
        return Response({
            'user': serializers.RegisterSerializer(user).data,
            'token': token
        })
