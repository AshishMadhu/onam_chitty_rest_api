import random
import pytz
import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from . mixins import TimeMixin

class Chitty(models.Model):
    ONAM_CHITTY = "on"
    CHITTY = 'ch'
    CHITTY_TYPES = (
        (ONAM_CHITTY, 'Onam Chittty'),
        (CHITTY, 'Usuall Chitty')
    )
    type = models.CharField(max_length = 2, choices = CHITTY_TYPES)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        type = self.get_type_display()
        return '{} - {}'.format(self.owner, type)

class Member(TimeMixin, models.Model):
    id = models.IntegerField(primary_key = True, editable = False, validators = [MaxValueValidator(9999), MinValueValidator(1000)])
    name = models.CharField(max_length = 100)
    date = models.DateTimeField(auto_now_add = True)
    chitty = models.ForeignKey(Chitty, on_delete = models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.name, self.id)

class Log(TimeMixin, models.Model):
    date = models.DateTimeField(auto_now_add = True)
    price_given = models.PositiveIntegerField()
    member = models.ForeignKey(Member, on_delete = models.CASCADE)
    
    # def get_now(self):
    #     """
    #     Returns now in utc
    #     """
    #     utc = pytz.timezone('utc')
    #     return datetime.datetime.utcnow().replace(tzinfo = utc)

    # def get_days(self, sec):
    #     return int(sec / 86400)
    
    # def get_hours(self, sec):
    #     return sec / 3600
    
    # def get_minutes(self, sec):
    #     return sec / 60

    # def get_total_seconds(self):
    #     now = self.get_now()
    #     diff = now - self.date
    #     return diff.total_seconds()

    # def get_time_difference(self):
    #     total_seconds = self.get_total_seconds()
    #     days = self.get_days(total_seconds)
    #     hours = self.get_hours(total_seconds)
    #     minutes = self.get_minutes(total_seconds)
    #     return {'days': days, 'hours': hours, 'minutes': minutes}
    
    # def get_time_stamp(self):
    #     now = self.get_now()
    #     return relativedelta(now, self.date)