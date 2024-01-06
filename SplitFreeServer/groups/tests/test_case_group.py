import datetime

from users_auth.tests.test_case_users import UsersTestCaseBase
from groups.models.group import GroupSerializer, Group


class GroupTestCaseBase(UsersTestCaseBase):
    group_title = 'My Group'
    group_name = 'my_group'

    def _get_path_with_name(self):
        return f'/group?name={self.group_name}'

    def setUp(self) -> None:
        super().setUp()

        serializer = GroupSerializer(data={
            'name': self.group_name,
            'title': self.group_title,
            'created': datetime.datetime.now(),
            'admin': self.user_admin.username,
            'members': [],
        })
        serializer.is_valid(raise_exception=True)
        self.group: Group = serializer.save()
        self.group.members.add(self.user_member)
        self.group.admin = self.user_admin
        self.group.save()

        self.group_id = self.group.pk
        self.path_with_name = self._get_path_with_name()

