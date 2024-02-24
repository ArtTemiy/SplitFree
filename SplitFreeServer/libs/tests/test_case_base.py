import dictdiffer
from django.test import TestCase
from rest_framework.test import APIClient


class TestCaseBase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def assertResponse(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code, response.data if hasattr(response, 'data') else '')

    def assertDicts(self, d1, d2):
        self.assertDictEqual(
            d1, d2,
            '\n' + '\n'.join(map(str, dictdiffer.diff(d1, d2)))
        )
