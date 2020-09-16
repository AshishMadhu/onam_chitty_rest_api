import pytz
from datetime import datetime, timedelta
from django.http import Http404
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from . import models
from . mixins import CustomPermissionDenied
from . custom_permission import IsUserChittyOwner, MemberObjectPermissions, LogPermissions
from . serializers import ChittySerializer, MemberSerializer, LogSerializer

class ChittyViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet
    ):
    queryset = models.Chitty.objects.all()
    serializer_class = ChittySerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner = user)

class MemberViewSet(CustomPermissionDenied, viewsets.ModelViewSet):
    """ 
    For more genuinity, api is restricted for patch, put, & delete requests.
     """
    serializer_class = MemberSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserChittyOwner, MemberObjectPermissions)
    authentication_classes = (TokenAuthentication, )
    filter_fields = ('name', )
    search_fields = ('^name', )
    ordering_fields = ('name', )

    def list(self, request, *args, **kwargs):
        try:
            models.Chitty.objects.get(id = request.GET.get('chitty_id'))
        except models.Chitty.DoesNotExist:
            raise Http404
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        chitty_id = self.request.GET.get('chitty_id', None)
        if chitty_id is None:
            return models.Member.objects.all()
        return models.Member.objects.filter(chitty_id = chitty_id)
    
    def perform_create(self, serializer):
        chitty = models.Chitty.objects.get(id = self.request.GET.get('chitty_id'))
        serializer.save(chitty = chitty)

class LogViewSet(CustomPermissionDenied, viewsets.ModelViewSet):
    """ 
    If you need to get list or POST, call the api with member_id
    else you need to pass id in kwargs and don't need to pass the member_id
     """
    serializer_class = LogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, LogPermissions)
    authentication_classes = (TokenAuthentication, )

    def get_starting_date(self):
        starting_date = None
        utc = pytz.timezone('utc')
        present = datetime.now(tz = utc)
        if present.month >= 9:
            starting_date = datetime(present.year, 8, 10).replace(tzinfo = utc)
        else:
            last_year = present.year - 1
            starting_date = datetime(last_year, 8, 10).replace(tzinfo = utc)
        return starting_date

    def get_total(self, request):
        starting_date = self.get_starting_date()
        return models.Log.objects.all().filter(
            member_id = request.GET.get('member_id'),
            date__gte = starting_date
        ).aggregate(total = Sum('price_given'))['total']
        
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = { 'results': serializer.data, 'total': self.get_total(request) }
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = { 'results': serializer.data, 'total': self.get_total(request) }
        return Response(data)

    def perform_create(self, serializer):
        member = models.Member.objects.get(id = self.request.GET.get('member_id'))
        serializer.save(member = member)
    
    def get_queryset(self):
        starting_date = self.get_starting_date()
        if self.request.GET.get('member_id', None) is None:
            return models.Log.objects.all()
        return models.Log.objects.filter(member_id = self.request.GET.get('member_id')).order_by('date')