from hashlib import sha256
from uuid import uuid4
from custom_exception import MinBalanceException

RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"


class User:

    def __init__(self, first_name, last_name, password, phone, email, role):
        self.first_name = first_name
        self.last_name = last_name
        self.__password = User.__valid_pass('password', password)
        self.phone = phone
        self.email = email
        self.id = uuid4().int
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
        # try:
        if len(str(password)) <= 4:
            raise ValueError(f"{name_var} length should be longer than 4")
        else:
            return sha256(str(password).encode('utf-8')).hexdigest()
        # except ValueError as e:
        #     return f'{YELLOW}("Hint:"){END} {e}'

    def __valid_username(self) -> str:
        pass

    @classmethod
    def register_new_user(cls, first_name, last_name, password, phone, email, role):
        """
        if username and password is valid call User class for initiate new User instance
        :param first_name: str form user input
        :param last_name: str form user input
        :param password: str from user input
        :param phone: str optional from user input
        :param email: str optional from user input
        :return: None
        """
        if first_name and last_name and password and phone and email and role:
            user = cls(first_name, last_name, password, phone, email, role)
            return user
        else:
            return f'first_name, last_name, password, phone, email, role is {RED}required{END}'

    def login(self, password) -> str:
        valid_pass = self.__valid_pass('login password', password)
        if valid_pass and self.__password == valid_pass:
            self.is_authenticated = True
            return f'login success as {self.full_name}'
        else:
            return f'login fail'


class BankAccount():
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

    def __check_min_balance(self, amount_to_withdraw) -> bool:
        return (self.__balance - amount_to_withdraw) <= BankAccount.MinBalance

    def withdraw(self, amount):  # برداشت وجه
        if amount <= 0:
            raise ValueError('amount must be positive')
        if self.__check_min_balance(amount):
            raise MinBalanceException("NOT Enough balance to withdraw!")
        else:
            self.__balance -= amount
            self.__balance -= self.WAGE_AMOUNT  # برداشت کارمزد

    def deposit(self) -> None:
        pass

    def get_balance(self) -> int:
        return self.__balance

    def change_wage(self) -> None:
        pass

    def change_min_balance(self) -> None:
        pass


class Passenger(User):
    def __init__(self):
        pass
