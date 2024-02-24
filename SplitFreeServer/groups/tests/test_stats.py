from _decimal import Decimal

from django.contrib.auth.models import User

from groups.models.group import Group
from split.models import SplitSerializer, Split
from split.tests.split_test_case import SplitTestCaseBase


class TestStats(SplitTestCaseBase):
    def setUp(self) -> None:
        super().setUp()
        self.group.members.add(self.user_other)
        Split.objects.all().delete()
        splits = SplitSerializer(data=[{
            'title': 't1',
            'description': '',
            'category': 'general',
            'group': self.group.name,
            'spends': [
                {
                    'user': self.user_admin.username,
                    'amount': -300,
                },
                {
                    'user': self.user_member.username,
                    'amount': 300,
                }
            ]
        }, {
            'title': 't2',
            'description': '',
            'category': 'general',
            'group': self.group.name,
            'spends': [
                {
                    'user': self.user_member.username,
                    'amount': -300,
                },
                {
                    'user': self.user_other.username,
                    'amount': 300,
                },
            ]
        }], many=True)
        splits.is_valid(raise_exception=True)
        splits.save()

    def test_get_stats(self):
        response = self.client_member.get(
            path=f'/group/stats?name={self.group.name}'
        )
        self.assertResponse(response)
        self.assertDicts(response.data, {
            'payouts': [{
                'user_from': self.user_other.username,
                'user_to': self.user_admin.username,
                'amount': Decimal(300),
            }]
        })
