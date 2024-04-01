import difflib
from _decimal import Decimal

from rest_framework.response import Response

from .split_test_case import SplitTestCaseBase
from ..models import Spend, Split


class SplitApiTests(SplitTestCaseBase):
    def test_get(self):
        response: Response = self.client_admin.get(
            path=f'/split?id={self.split.pk}'
        )
        self.assertResponse(response)
        expected = {
            'id': self.split.pk,
            'title': self.split.title,
            'description': self.split.description,
            'category': self.split.category,
            'group': self.split.group.name,
            'spends': [s for s in response.data['spends'] if s in
                       [{
                           'user': spend.user.username,
                           'amount': spend.amount,
                       } for spend in Spend.objects.filter(split=self.split)]
                       ],
            'amount': sum([abs(s.amount) for s in self.split.spends.all()]) / 2,
        }
        self.assertDictEqual(
            dict(response.data),
            expected,
        )

    def test_create(self):
        title2 = 'My Title'

        response: Response = self.client_admin.post(
            path='/split',
            data={
                'title': title2,
                'description': '',
                'group': self.group.name,
                'spends': [
                    {
                        'user': self.user_admin.username,
                        'amount': Decimal('-12.34'),
                    },
                    {
                        'user': self.user_member.username,
                        'amount': Decimal('12.34'),
                    }
                ],
                'category': 'gifts'
            },
        )
        self.assertResponse(response)
        self.assertDicts(
            self.client_admin.get(path=f'/split?id={response.data["id"]}').data,
            {
                'id': response.data['id'],
                'title': title2,
                'description': '',
                'group': self.group.name,
                'spends': [
                    {
                        'user': self.user_admin.username,
                        'amount': Decimal('-12.34'),
                    },
                    {
                        'user': self.user_member.username,
                        'amount': Decimal('12.34'),
                    }
                ],
                'category': 'gifts',
                'amount': Decimal('12.34'),
            }
        )

    def create_disbalance(self):
        self.assertResponse(self.client.post(
            path='/split',
            data={
                'title': 'asd',
                'description': '',
                'group': self.group.name,
                'category': 'general',
                'spends': [{
                    'user': self.user_admin.username,
                    'amount': 12.34,
                }]
            }
        ), status_code=400)

    def test_update(self):
        title2 = 'My Title 2'

        spends = set(self.split.spends.all())
        self.assertResponse(
            self.client_member.put(
                path=f'/split?id={self.split.pk}',
                data={
                    'title': title2
                }
            )
        )
        self.assertEqual(title2, Split.objects.get(pk=self.split.pk).title)
        self.assertEqual(spends, set(Split.objects.get(pk=self.split.pk).spends.all()))

    def test_update_spends(self):
        self.assertResponse(self.client_member.put(
            path=f'/split?id={self.split.pk}',
            data={
                'spends': [
                    {
                        'user': self.user_admin.username,
                        'amount': -12.34,
                    },
                    {
                        'user': self.user_member.username,
                        'amount': 12.34,
                    }
                ]
            }
        ))
        self.assertEqual(
            2,
            Split.objects.get(pk=self.split.pk).spends.count(),
            Split.objects.get(pk=self.split.pk).spends.all()
        )
        self.assertEqual(2, Spend.objects.count())

    def test_delete(self):
        pass
