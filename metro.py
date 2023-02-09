from hashlib import sha256
from uuid import uuid4
from custom_exception import (
    MinBalanceException,
    InvalidTimeFormatException,
    InvalidTimePeriod,
    InvalidPriceValue,
    InvalidPhoneFormat,
    InvalidPassword,
)
from datetime import datetime
from typing import Tuple
import re

RED = "\033[0;31m"
REDB = "\u001b[41;1m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"


class User:

    def __init__(self, first_name, last_name, password, phone, email, role):
        self.user_id = None
        self.first_name = first_name
        self.last_name = last_name
        self.__password = User.__valid_pass('password', password)
        self.phone = phone
        self.email = email
        self.uuid = str(uuid4().int)
        self.role_id = role
        self.is_authenticated = False
        self.have_bank_account = False

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_info(self) -> str:
        pass

    @staticmethod
    def __valid_pass(name_var: str, password: str) -> str:
        """
        check password validation and return sha256(password)
        :param name_var: variable name show in message
        :param password: user input password
        :return: str
        """
        password_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.match(password_regex, password):
            raise InvalidPassword(f"{name_var} minimum 8 characters, at least one letter and one number")
        else:
            return sha256(str(password).encode('utf-8')).hexdigest()

    @classmethod
    def register_new_user(cls, first_name, last_name, password, phone, email, role):
        """
        if username and password is valid call User class for initiate new User instance
        :param first_name: str form user input
        :param last_name: str form user input
        :param password: str from user input
        :param phone: str from user input
        :param email: str from user input
        :param role: int from user input (1:regular_user, 2:admin)
        :return: User
        """
        phone_regex = r'^09[0-9]{9}$'
        if not re.match(phone_regex, phone):
            raise InvalidPhoneFormat('phone incorrect. valid format: 09123456789')

        user = cls(first_name, last_name, password, phone, email, role)
        return user

    @classmethod
    def login(cls, password, hash_password) -> bool:
        valid_pass = cls.__valid_pass('login password', password)
        if valid_pass and hash_password == valid_pass:
            # self.is_authenticated = True
            # return f'login success as {self.full_name}'
            return True
        else:
            return False

    @staticmethod
    def insert_to_database(user, cur):
        if user.role_id == 2:
            query = """INSERT INTO user (
                        first_name, 
                        last_name, 
                        password, 
                        phone, 
                        email, 
                        role_id, 
                        uuid,
                        is_authenticated, 
                        have_bank_account) VALUES (?,?,?,?,?,?,?,?,?)
                        """
            data = (user.first_name,
                    user.last_name,
                    user.__password,
                    user.phone,
                    user.email,
                    user.role_id,
                    user.uuid,
                    user.is_authenticated,
                    user.have_bank_account
                    )
            cur.execute(query, data)
            return cur.lastrowid
        elif user.role_id == 1:
            cur.execute('BEGIN TRANSACTION')
            query = """INSERT INTO user (
                                    first_name, 
                                    last_name, 
                                    password, 
                                    phone, 
                                    email, 
                                    role_id, 
                                    uuid,
                                    is_authenticated, 
                                    have_bank_account) VALUES (?,?,?,?,?,?,?,?,?)
                                    """
            data = (user.first_name,
                    user.last_name,
                    user.__password,
                    user.phone,
                    user.email,
                    user.role_id,
                    user.uuid,
                    user.is_authenticated,
                    user.have_bank_account
                    )
            cur.execute(query, data)
            return cur.lastrowid


class BankAccount:
    WAGE_AMOUNT = 100
    MinBalance = 1000

    def __init__(self, owner: User, balance: int) -> None:
        self.owner = owner
        self.__balance = balance

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        # try:
        if isinstance(value, User):
            self.__owner = User
        else:
            raise TypeError(f'owner must be a User')
        # except TypeError as e:
        #     print(f'ERR: {e}')

    @property
    def balance(self):
        return self.__balance

    @staticmethod
    def __check_min_balance(balance, amount_to_withdraw) -> bool:
        return (balance - amount_to_withdraw) <= BankAccount.MinBalance

    @staticmethod
    def withdraw(balance, amount):  # برداشت وجه
        if amount <= 0:
            raise ValueError('amount must be positive')
        if BankAccount.__check_min_balance(balance, amount):
            raise MinBalanceException("NOT Enough balance to withdraw!")
        else:
            balance -= amount
            balance -= BankAccount.WAGE_AMOUNT  # برداشت کارمزد
            return balance

    def insert_to_database(self, user, cur):
        query = """
            INSERT INTO bank_account (
            owner_id, 
            balance
            ) VALUES (?,?)
        """
        data = (user.user_id, self.__balance)
        cur.execute(query, data)
        query = """
            UPDATE user
            SET have_bank_account=?
            WHERE user_id=?
        """
        data = (1, user.user_id)
        cur.execute(query, data)
        # return cur.lastrowid

    @staticmethod
    def deposit(balance, amount) -> int:
        if amount <= 0:
            raise ValueError('amount must be positive')
        else:
            return balance + amount

    def get_balance(self) -> int:
        self.__balance -= self.WAGE_AMOUNT  # برداشت کارمزد
        return self.__balance

    def change_wage(self) -> None:
        pass

    def change_min_balance(self) -> None:
        pass


class Travel:
    def __init__(self, price, start_time, end_time):
        self.price = price
        self.start_time = start_time
        self.end_time = end_time
        self.active = Travel.is_active(end_time)

    @staticmethod
    def is_active(t):
        t = datetime.strptime(t, '%Y/%m/%d %H:%M')
        if t >= datetime.now():
            return 1
        return 0

    @staticmethod
    def valid_data(t: Tuple[str, str], p: int):
        start, end = list(map(lambda str_time: datetime.strptime(str_time, '%Y/%m/%d %H:%M'), t))
        if start > end:
            raise InvalidTimePeriod("start time must be lower than end time")
        if not isinstance(p, int) or p <= 0:
            raise InvalidPriceValue("price value must be positive number")
        is_active = Travel.is_active(t[1])
        return p, t[0], t[1], is_active


class Cart:
    def __init__(self, cart_type, credit=None, expire_date=None):
        self.cart_type = cart_type
        self.credit = credit
        self.expire_date = expire_date

    @classmethod
    def create_cart(cls, cart_type, credit, expire_date):
        if cart_type == 1:
            return cls(cart_type, credit, None)
        elif cart_type == 2:
            return cls(cart_type, credit, None)
        elif cart_type == 3:
            return cls(cart_type, credit, expire_date)
