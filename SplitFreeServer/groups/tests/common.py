import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from groups.models.group import GroupSerializer, Group


class GroupTestBase(TestCase):
    group_title = 'My Group'
    group_name = 'my_group'

    def assertResponse(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code, response.data if hasattr(response, 'data') else '')

    def _get_path_with_name(self):
        return f'/group?name={self.group_name}'

    def setUp(self) -> None:
        self.author = User.objects.create_user('user_author')
        self.author.set_password('asd1')
        self.author.save()

        self.user = User.objects.create_user('user_other')
        self.user.set_password('asd2')
        self.user.save()

        serializer = GroupSerializer(data={
            'name': self.group_name,
            'title': self.group_title,
            'created': datetime.datetime.now(),
            # 'admin': {'username': self.author.username},
            'admin': self.author.username,
            'members': [],
        })
        serializer.is_valid(raise_exception=True)
        self.group: Group = serializer.save()
        self.group.members.add(self.user)
        self.group.admin = self.author
        self.group.save()

        self.group_id = self.group.pk
        self.path_with_name = self._get_path_with_name()

        self.auth_token = Token.objects.create(user=self.author)

        self.client = APIClient(headers={
            'Authorization': f'Token {self.auth_token}'
        })
