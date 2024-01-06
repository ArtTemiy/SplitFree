from .test_case_users import UsersTestCaseBase


class HappyPassTest(UsersTestCaseBase):
    def test(self):
        self.assertTrue(True)
