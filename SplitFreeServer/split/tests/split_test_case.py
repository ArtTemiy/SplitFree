from django.contrib.auth.models import User

from groups.tests.test_case_group import GroupTestCaseBase
from split.models import SplitSerializer, SpendSerializer


class SplitTestCaseBase(GroupTestCaseBase):
    def setUp(self) -> None:
        super().setUp()
        split_serializer = SplitSerializer(data={
            'title': 'Ужин',
            'description': 'Ужин на двоих',
            'category': 'dinner',
            'group': self.group.name,
            'spends': [
                {
                    'user': self.user_admin.username,
                    'amount': 123,
                },
                {
                    'user': self.user_admin.username,
                    'amount': -23,
                },
                {
                    'user': self.user_member.username,
                    'amount': -100,
                },
            ]
        })
        split_serializer.is_valid(raise_exception=True)
        self.split = split_serializer.save()
