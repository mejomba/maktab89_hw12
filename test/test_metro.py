import unittest
from sqlite3_contextmanager import CreateUserContextManager, CreateBankAccountContextManager
from metro import User


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


class TestCreateBankAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.test_set1 = ['jafar', 15000]
        self.test_set2 = [User('mojtaba', 'aminzadeh', '12345', '0936', 'abc@gmail.com'), 15000]

    def test_create_bank_account_context_manager_test_set1(self):
        with CreateBankAccountContextManager(self.test_set1[0]) as CB:
            CB.create_bank_account(self.test_set1[1])
        self.assertEqual(CB.err, f'create bank account fail\nHint: {CB.exc_val}')
        self.assertEqual(CB.exc_type, TypeError)
        self.assertIs(CB.result, None)

    def test_create_bank_account_context_manager_test_set2(self):
        with CreateBankAccountContextManager(self.test_set2[0]) as CB:
            CB.create_bank_account(self.test_set2[1])
        self.assertIs(CB.err, None)
        self.assertIs(CB.exc_type, None)
        self.assertEqual(CB.result, f'create bank account for {CB.user.full_name} successfully')


if __name__ == "__main__":
    unittest.main()