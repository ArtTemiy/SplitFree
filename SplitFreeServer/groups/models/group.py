import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE

from rest_framework import serializers
from rest_framework.fields import CharField, SlugField
from rest_framework.relations import SlugRelatedField

from auth.models import UserSerializer


class Group(models.Model):
    name = models.CharField(max_length=128, blank=False)
    title = models.CharField(max_length=1024, blank=False)
    created = models.DateTimeField(blank=False)
    admin = models.ForeignKey(User, on_delete=CASCADE, related_name='admin')
    members = models.ManyToManyField(User, related_name='members')

    class Meta:
        verbose_name = "group"
        verbose_name_plural = "groups"

    def __str__(self):
        return f'{self.title}, ({",".join(u.username for u in self.members.all())})'


def get_username(obj):
    return obj.username


class GroupSerializer(serializers.ModelSerializer):
    name = SlugField(max_length=128, min_length=3, allow_blank=False)
    admin = SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    members = SlugRelatedField(queryset=User.objects.all(), slug_field='username', many=True)

    class Meta:
        model = Group
        fields = '__all__'
