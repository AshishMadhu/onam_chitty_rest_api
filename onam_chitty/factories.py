import random
import datetime
import factory
import factory.fuzzy
from user.factories import UserFactory
from . import models
from . import serializers

choices = [x[0] for x in models.Chitty.CHITTY_TYPES]
class ChittyFactory(factory.django.DjangoModelFactory):
    type = factory.fuzzy.FuzzyChoice(choices=choices)
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Chitty

class MemberFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('user_name')
    date = factory.fuzzy.FuzzyDate(datetime.date(2008, 1, 1))
    chitty = factory.SubFactory(ChittyFactory)

    @factory.lazy_attribute
    def id(self):
        return serializers.MemberSerializer.generate_id()

    class Meta:
        model = models.Member

class LogFactory(factory.django.DjangoModelFactory):
    date = factory.fuzzy.FuzzyDateTime(datetime.datetime(2018, 11, 1, tzinfo = datetime.timezone.utc))
    price_given = factory.fuzzy.FuzzyInteger(low = 100, high = 1000)
    member = factory.SubFactory(MemberFactory)

    class Meta:
        model = models.Log