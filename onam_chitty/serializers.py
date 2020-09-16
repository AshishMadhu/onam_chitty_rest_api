import random
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from . import models

class ChittySerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(models.Chitty.CHITTY_TYPES)
    owner = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = models.Chitty
        fields = "__all__"

class MemberSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    chitty = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = models.Member
        fields = "__all__"
    
    @classmethod
    def generate_id(cls):
        id = None
        unique = False
        while(not unique):
            id = random.randint(999, 9999)
            try:
                models.Member.objects.get(id = id)
                unique = False
            except models.Member.DoesNotExist:
                unique = True
        return id

    def get_id(self, obj):
        return self.generate_id()

class LogSerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(read_only = True)
    price_given = serializers.IntegerField(validators = [MaxValueValidator(10000), MinValueValidator(10)])

    class Meta:
        model = models.Log
        fields = "__all__"