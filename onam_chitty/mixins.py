import pytz
import datetime
from dateutil.relativedelta import relativedelta
from rest_framework import permissions
from rest_framework import exceptions

class CustomPermissionDenied(object):
    def permission_denied(self, request, message = None):
        if request.method in permissions.SAFE_METHODS:
            pass
        elif request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=message)

class TimeMixin(object):
    
    def get_now(self):
        """
        Returns now in utc
        """
        utc = pytz.timezone('utc')
        return datetime.datetime.utcnow().replace(tzinfo = utc)

    def get_days(self, sec):
        return int(sec / 86400)
    
    def get_hours(self, sec):
        return sec / 3600
    
    def get_minutes(self, sec):
        return sec / 60

    def get_total_seconds(self):
        now = self.get_now()
        diff = now - self.date
        return diff.total_seconds()

    def get_time_difference(self):
        total_seconds = self.get_total_seconds()
        days = self.get_days(total_seconds)
        hours = self.get_hours(total_seconds)
        minutes = self.get_minutes(total_seconds)
        return {'days': days, 'hours': hours, 'minutes': minutes}
    
    def get_time_stamp(self):
        now = self.get_now()
        return relativedelta(now, self.date)
