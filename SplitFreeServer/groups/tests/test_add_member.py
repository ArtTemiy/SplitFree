from django.contrib.auth.models import User

from groups.models.group import Group
from .test_case_group import GroupTestCaseBase


class AdditionalViewTests(GroupTestCaseBase):
    def test_add_members(self):
        usernames = ['new_user1', 'new_user2']
        for un in usernames:
            o = User.objects.create_user(username=un)
            o.save()
        self.assertResponse(
            self.client_admin.post(
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
            self.client_admin.delete(
                path=f'/group/members?name={self.group_name}',
                data={
                    'members': [self.user_member.username],
                },
                format='json'
            )
        )
        self.assertEqual(Group.objects.get(name=self.group_name).members.count(), 0)
