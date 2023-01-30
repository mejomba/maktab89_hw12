import unittest
from sqlite3_contextmanager import CreateUserContextManager


class TestCreateUser(unittest.TestCase):
    def setUp(self) -> None:
        self.test_set1 = ['mojtaba', 'aminzadeh', '12345', '0936', 'abc@gmail.com']
        self.test_set2 = ['zahra', 'jafari', '1234', '0936', 'xyz@gmail.com']
        # self.test_set3 = ['mojtaba', 'aminzadeh', '12345', '0936', 'abc@gmail.com']
        # self.test_set4 = ['mojtaba', 'aminzadeh', '12345', '0936', 'abc@gmail.com']

    def test_create_bank_account_context_manager(self):
        with CreateUserContextManager() as CU:
            CU.create_user(*self.test_set1)
        self.assertEqual(CU.user.full_name, 'mojtaba aminzadeh')
        self.assertEqual(CU.result, f'create user {CU.user.full_name} successfully')

        with CreateUserContextManager() as CU:
            CU.create_user(*self.test_set2)
        self.assertIs(CU.user, None)
        self.assertEqual(CU.err, f'create user fail\nHint: {CU.exc_val}')