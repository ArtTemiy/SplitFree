from split.models import Spend, Split, SplitSerializer, SpendSerializer
from split.tests.split_test_case import SplitTestCaseBase


class TestSplitSerializer(SplitTestCaseBase):
    def test_init_base(self):
        self.assertEqual(
            Spend.objects.filter(split=self.split).count(),
            3
        )

    def test_update(self):
        ss = SplitSerializer(
            instance=self.split,
            data={
                'spends': [
                    {
                        'user': self.user_admin.username,
                        'amount': -123.4,
                    },
                    {
                        'user': self.user_member.username,
                        'amount': 123.4,
                    }
                ]
            },
            partial=True
        )
        ss.is_valid(raise_exception=True)
        ss.save()
        self.assertEqual(Spend.objects.count(), 2, Spend.objects.all())
