import unittest
from sqlite3_contextmanager import CreateUserContextManager, CreateBankAccountContextManager
from metro import User, BankAccount, Travel, Cart
from custom_exception import InvalidPassword, InvalidPhoneFormat, MinBalanceException
from hashlib import sha256
import sqlite3
from sqlite3_contextmanager import create_tables


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

        self.user = User.register_new_user(*self.register_new_user_test_set_1)
        self.conn = None
        self.cur = None

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
        error = "login password minimum 8 characters, at least one letter and one number"
        self.assertEqual(password_err.exception.args[0], error)

    def test_insert_to_database(self):
        create_tables(db_name='db_for_test')
        self.conn = sqlite3.connect('db_for_test')
        self.cur = self.conn.cursor()
        res = User.insert_to_database(user=self.user, cur=self.cur)
        self.assertNotEqual(res, 0)
        self.assertEqual(res, self.cur.lastrowid)


class TestBankAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.mojtaba = User('mojtaba', 'aminzadeh', 'a1234567', '09112345678', 'mojtaba@mail.com', 1)
        self.ahmad = User('ahmad', 'safari', 'a1234567', '09112345678', 'ahmad@mail.com', 1)
        self.mojtaba_acc = BankAccount(self.mojtaba, 50000)
        self.ahmad_acc = BankAccount(self.ahmad, 20000)
        BankAccount.WAGE_AMOUNT = 600
        BankAccount.MinBalance = 5000

    def test_withdraw(self):
        with self.assertRaises(MinBalanceException) as error:
            self.mojtaba_acc.withdraw(self.mojtaba_acc.balance, 46000)
        self.assertTrue("NOT Enough balance to withdraw!" in str(error.exception))

        amount_to_withdraw = 10000
        res = self.mojtaba_acc.withdraw(self.mojtaba_acc.balance, amount_to_withdraw)
        self.assertEqual(res, self.mojtaba_acc.balance - amount_to_withdraw - BankAccount.WAGE_AMOUNT)

        with self.assertRaises(ValueError) as error2:
            self.mojtaba_acc.withdraw(self.mojtaba_acc.balance, -10000)
        self.assertTrue("amount must be positive" in str(error2.exception))

    def test_deposit(self):
        res = BankAccount.deposit(self.mojtaba_acc.balance, 1000)
        self.assertEqual(res, self.mojtaba_acc.balance + 1000)

        with self.assertRaises(ValueError) as error:
            BankAccount.deposit(self.mojtaba_acc.balance, -1000)
        self.assertEqual(str(error.exception), 'amount must be positive')

    def test_insert_to_database(self):
        create_tables(db_name='db_for_test')
        self.conn = sqlite3.connect('db_for_test')
        self.cur = self.conn.cursor()
        self.mojtaba_acc.insert_to_database(self.mojtaba, self.cur)
        self.assertNotEqual(self.cur.lastrowid, 0)

    def test_get_balance(self):
        self.assertEqual(self.mojtaba_acc.get_balance(), 50000 - BankAccount.WAGE_AMOUNT)


class TestTravel(unittest.TestCase):
    def setUp(self) -> None:
        self.test_set_1 = [1200, '2020/12/10 10:10', '2020/12/10 10:30']
        self.test_set_2 = [1200, '2023/10/10 10:10', '2023/12/10 10:30']
        self.travel_1 = Travel(*self.test_set_1)
        self.travel_2 = Travel(*self.test_set_2)

    def test_is_active(self):
        res = Travel.is_active(self.travel_1.end_time)
        self.assertEqual(res, 0)

        res = Travel.is_active(self.travel_2.end_time)
        self.assertEqual(res, 1)

    def test_valid_data(self):
        res = Travel.valid_data((self.travel_1.start_time, self.travel_1.end_time), self.travel_1.price)
        self.assertEqual(res, (self.travel_1.price, self.travel_1.start_time, self.travel_1.end_time, 0))

        res = Travel.valid_data((self.travel_2.start_time, self.travel_2.end_time), self.travel_2.price)
        self.assertEqual(res, (self.travel_2.price, self.travel_2.start_time, self.travel_2.end_time, 1))


class TestCart(unittest.TestCase):
    def setUp(self) -> None:
        self.test_set_1 = [1, 1000, '2023/12/12']
        self.test_set_2 = [2, 1000, '2023/12/12']
        self.test_set_3 = [3, 1000, '2023/12/12']

    def test_create_cart(self):
        res = Cart.create_cart(*self.test_set_1)
        self.assertEqual((res.cart_type, res.credit, res.expire_date), (1, 1000, None))
        self.assertIsInstance(res, Cart)

        res = Cart.create_cart(*self.test_set_2)
        self.assertEqual((res.cart_type, res.credit, res.expire_date), (2, 1000, None))
        self.assertIsInstance(res, Cart)

        res = Cart.create_cart(*self.test_set_3)
        self.assertEqual((res.cart_type, res.credit, res.expire_date), (3, 1000, '2023/12/12'))
        self.assertIsInstance(res, Cart)


if __name__ == "__main__":
    unittest.main()
