# import datetime
# from django.db import models
# from django.contrib.auth.models import User
#
# from rest_framework import serializers
#
#
# class Group(models.Model):
#     title = models.CharField(max_length=1024)
#     members = models.ManyToManyField(User)
#     created = models.DateTimeField()
#
#     class Meta:
#         verbose_name = "group"
#         verbose_name_plural = "groups"
#
#     def __str__(self):
#         return self.title
#
#
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = 'all'
#
#     def create(self, validated_data):
#         o = Group.objects.create(
#             {f: validated_data[f] for f in [
#                 'title'
#             ]},
#             created=datetime.datetime.now(),
#             members=[validated_data['author_id']]
#         )
#         return o
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         return instance
#
#     def add_user(self):
#         pass
#
#     def remove_user(self):
#         pass
