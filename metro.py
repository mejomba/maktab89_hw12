from hashlib import sha256
from uuid import uuid4

RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"


class User:

    def __init__(self, first_name, last_name, password, phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.__password = User.__valid_pass('password', password)
        self.phone = phone
        self.email = email
        self.id = uuid4().int
        print("id in init", self.id)

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
    def register_new_user(cls, first_name, last_name, password, phone, email):
        """
        if username and password is valid call User class for initiate new User instance
        :param first_name: str form user input
        :param last_name: str form user input
        :param password: str from user input
        :param phone: str optional from user input
        :param email: str optional from user input
        :return: None
        """
        if first_name and last_name and password and phone and email:
            user = cls(first_name, last_name, password, phone, email)
            return user
        else:
            return f'first_name, last_name, password, phone, email is {RED}required{END}'

    def login(self) -> "User":
        pass


class BankAccount():
    wage_amount = 100
    min_balance = 1000

    def __init__(self, owner: User, balance: int) -> None:
        self.owner = owner
        self.__balance = balance

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        try:
            if isinstance(value, User):
                self.__owner = User
            else:
                raise TypeError(f'{RED}owner must be a User{END}')
        except TypeError as e:
            print(f'ERR: {e}')

    @property
    def balance(self):
        return self.__balance

    def __check_min_balance(self) -> bool:
        pass

    def withdraw(self) -> None:
        pass

    def deposit(self) -> None:
        pass

    def get_balance(self) -> int:
        pass

    def change_wage(self) -> None:
        pass

    def change_min_balance(self) -> None:
        pass


class Passenger(User):
    def __init__(self):
        pass
