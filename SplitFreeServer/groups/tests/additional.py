from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token

from groups.models.group import Group, GroupSerializer
from .common import GroupTestBase


class AdditionalViewTests(GroupTestBase):
    def test_add_members(self):
        usernames = ['new_user1', 'new_user2']
        username_pks = []
        for un in usernames:
            o = User.objects.create_user(username=un)
            o.save()
            username_pks.append(o.pk)
        self.assertResponse(
            self.client.post(
                path=f'/group/members?name={self.group_name}',
                data={
                    'members': usernames,
                },
                format='json'
            )
        )

        members = [member.username for member in self.group.members.all()]
        for un in usernames:
            self.assertIn(un, members)

    def test_delete_members(self):
        self.assertResponse(
            self.client.delete(
                path=f'/group/members?name={self.group_name}',
                data={
                    'members': [self.user.username],
                },
                format='json'
            )
        )
        self.assertEqual(Group.objects.get(name=self.group_name).members.count(), 0)
