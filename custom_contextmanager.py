from metro import User, BankAccount
from admin import Admin
import pickle

RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"


class CreateUserContextManager:
    def __init__(self):
        self.user = None
        self.bank_account = None
        self.err = None
        self.result = None

    def __enter__(self):
        return self

    def create_user(self, first_name, last_name, password, phone, email):
        self.user = User.register_new_user(first_name, last_name, password, phone, email)
        with open('users.pickle', 'ab') as pkl:
            pickle.dump(self.user, pkl)
        self.result = f'user {GREEN}{self.user.full_name}{END} create and save successfully'
        print('after user create')

    def create_user_bank_account(self, balance):
        self.bank_account = BankAccount(self.user, balance)
        with open('bank.pickle', 'ab') as pkl:
            pickle.dump(self.bank_account, pkl)
        self.result = f'bank account create for user {GREEN}{self.user.full_name}{END} and save successfully'

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.err = f'{RED}user register fail{END}\n{YELLOW}Hint:{END} {exc_val}'
        return True


class SelectUserContextManager:
    def __init__(self):
        self.user = None
        self.err = None
        self.result = None

    def __enter__(self):
        return self

    def select_user(self, user_id):
        with open('users.pickle', 'rb') as pkl:
            self.user = None
            while True:
                try:
                    self.user = pickle.load(pkl)
                    if self.user.id == user_id:
                        self.result = f'find: {self.user.full_name} for id={self.user.id}'
                        return self.user
                except EOFError:
                    self.user = None
                    self.result = f'no user with id "{user_id}"'
                    return

    def login_user(self, password):
        # if self.user:
        self.result = User.login(self.user, password)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # if exc_val:
        #     self.err = f'{RED}user register fail{END}\n{YELLOW}Hint:{END} {exc_val}'
        return True
        pass