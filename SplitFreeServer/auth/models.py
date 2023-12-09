from django.contrib.auth.models import User
from django.db import models
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
