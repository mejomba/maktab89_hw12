import unittest
from sqlite3_contextmanager import CreateUserContextManager, CreateBankAccountContextManager
from metro import User
from custom_exception import InvalidPassword, InvalidPhoneFormat
from hashlib import sha256


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


class TestUserClass(unittest.TestCase):
    def setUp(self) -> None:
        self.register_new_user_test_set_1 = ['mojtaba', 'aminzadeh', 'a1234567', '09112345678', 'mojtaba@mail.com', 1]
        self.register_new_user_test_set_2 = ['mojtaba', 'aminzadeh', 'a1234567', '0911234567', 'mojtaba@mail.com', 1]
        self.register_new_user_test_set_3 = ['mojtaba', 'aminzadeh', '123456', '09112345678', 'mojtaba@mail.com', 1]
        self.login_test_set1 = ['a1234567', sha256('a1234567'.encode('utf-8')).hexdigest()]
        self.login_test_set2 = ['1234567a', sha256('a1234567'.encode('utf-8')).hexdigest()]
        self.login_test_set3 = ['123', sha256('a1234567'.encode('utf-8')).hexdigest()]

    def test_register_new_user(self):
        self.assertIsInstance(User.register_new_user(*self.register_new_user_test_set_1), User)

        with self.assertRaises(InvalidPhoneFormat) as phone_err:
            User.register_new_user(*self.register_new_user_test_set_2)
        self.assertEqual(phone_err.exception.args[0], 'phone incorrect. valid format: 09123456789')

        with self.assertRaises(InvalidPassword) as password_err:
            User.register_new_user(*self.register_new_user_test_set_3)
        error = "password minimum 8 characters, at least one letter and one number"
        self.assertEqual(password_err.exception.args[0], error)

    def test_login(self):
        self.assertTrue(User.login(*self.login_test_set1))
        self.assertFalse(User.login(*self.login_test_set2))

        with self.assertRaises(InvalidPassword) as password_err:
            User.login(*self.login_test_set3)
        error = "password minimum 8 characters, at least one letter and one number"
        self.assertEqual(password_err.exception.args[0], error)

if __name__ == "__main__":
    unittest.main()