from rest_framework.response import Response

from .split_test_case import SplitTestCaseBase
from ..models import Spend, Split


class SplitApiTests(SplitTestCaseBase):
    def test_get(self):
        response: Response = self.client_admin.get(
            path=f'/split?id={self.split.pk}'
        )
        self.assertResponse(response)
        self.assertDictEqual(response.data, {
            'id': self.split.pk,
            'title': self.split.title,
            'description': self.split.description,
            'category': self.split.category,
            'group': self.split.group.name,
            'spends': [s for s in response.data['spends'] if s in
                       [{
                           'user': spend.user.username,
                           'amount': f'{spend.amount:.2f}',
                       } for spend in Spend.objects.filter(split=self.split)]
                       ],
            'amount': sum([abs(s.amount) for s in self.split.spends.all()]) / 2,
        })

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
                        'amount': '-1234.00',
                    },
                    {
                        'user': self.user_member.username,
                        'amount': 1234,
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
                        'amount': '-1234.00',
                    },
                    {
                        'user': self.user_member.username,
                        'amount': '1234.00',
                    }
                ],
                'category': 'gifts',
                'amount': ' 1234.00',
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
                    'amount': 1234,
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
                        'amount': -1234,
                    },
                    {
                        'user': self.user_member.username,
                        'amount': 1234,
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
