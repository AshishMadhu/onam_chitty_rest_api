from django.urls import reverse
from rest_framework import permissions
from . models import Chitty, Member

class IsUserChittyOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if view.kwargs.get('pk', None) is None:
                assert 'chitty_id' in request.GET, 'Pass chitty_id in url'
            if request.method == "POST":
                request.user.chitty_set.get(id = request.GET.get('chitty_id'))
            return True
        except AssertionError as msg:
            self.message = msg
            return False
        except Chitty.DoesNotExist:
            return False

class MemberObjectPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return False
        methods = ('PATCH', 'PUT')
        total_seconds = obj.get_total_seconds()
        minutes = obj.get_minutes(total_seconds)
        print(minutes)
        if request.method in methods:
            try:
                request.user.chitty_set.get(id = obj.chitty.id)
                if minutes >= 5:
                    self.message = "You cannot change the price after 5 min."
                    return False
                else:
                    return True
            except Chitty.DoesNotExist:
                return False
        else:
            return True

class LogPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return False
        try:
            if view.kwargs.get('pk', None) is None:
                assert 'member_id' in request.GET, 'Pass member_id in url'
            if request.method == "POST":
                chitty_id = Member.objects.get(id = request.GET.get('member_id')).chitty.id
                request.user.chitty_set.get(id = chitty_id)
            return True
        except AssertionError as msg:
            self.message = msg
            return False
        except Member.DoesNotExist:
            self.message = 'Invalid member_id'
            return False
        except Chitty.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        total_seconds = obj.get_total_seconds()
        minutes = obj.get_minutes(total_seconds)
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            request.user.chitty_set.get(id = obj.member.chitty.id)
            if minutes >= 5:
                self.message = "You cannot change the price after 5 min."
                return False
            else:
                return True
        except Chitty.DoesNotExist:
            return False