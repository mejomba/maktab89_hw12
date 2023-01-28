from hashlib import sha256


RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"


class User:
    id = 0

    def __init__(self, first_name, last_name, password, phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.__password = password
        self.phone = phone
        self.email = email

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
        try:
            if len(str(password)) >= 4:
                raise ValueError(f"{name_var} length should be longer than 3")
            else:
                return sha256(str(password).encode('utf-8')).hexdigest()
        except ValueError as e:
            print(f'{YELLOW}("Hint:"){END}', e)

    def __valid_username(self) -> str:
        pass

    @classmethod
    def register_new_user(cls):
        pass

    def login(self) -> "User":
        pass

