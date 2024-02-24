from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from libs.tests.test_case_base import TestCaseBase


class UsersTestCaseBase(TestCaseBase):
    def setUp(self) -> None:
        self.maxDiff = None

        self.user_admin = User.objects.create_user(username='user_author', password='asd')
        self.user_admin.save()

        self.user_member = User.objects.create_user(username='user_member', password='asd2')
        self.user_member.save()

        self.user_other = User.objects.create_user(username='user_other', password='asd3')
        self.user_other.save()

        self.user_admin_auth_token = Token.objects.create(user=self.user_admin)
        self.client_admin = APIClient(headers={
            'Authorization': f'Token {self.user_admin_auth_token}'
        })
        self.user_member_auth_token = Token.objects.create(user=self.user_member)
        self.client_member = APIClient(headers={
            'Authorization': f'Token {self.user_member_auth_token}'
        })
        self.user_other_auth_token = Token.objects.create(user=self.user_other)
        self.client_other = APIClient(headers={
            'Authorization': f'Token {self.user_other_auth_token}'
        })
