from metro import User, BankAccount
from admin import Admin
import settings
import pickle
from sqlite3_contextmanager import insert_sql

RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"


def read_all_data(file_name):
    all_data = []
    with open(file_name, 'rb') as file:
        while True:
            try:
                all_data.append(pickle.load(file))
            except EOFError:
                return all_data


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
        print('after user create')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.err = f'{RED}user register fail{END}\n{YELLOW}Hint:{END} {exc_val}'
            return True
        if not exc_type and self.user.have_bank_account:
            with open('users.pickle', 'ab') as pkl:
                pickle.dump(self.user, pkl)
            self.result = f'user {GREEN}{self.user.full_name}{END} create and save successfully'

            if settings.DEBUG:
                with open('debug.txt', 'a') as file:
                    print(self.user.full_name, self.user.id, file=file)
        return True


class CreateBankAccountContextManager:
    def __init__(self, user: User):
        self.bank_account = None
        self.user = user
        self.err = None
        self.result = None

    def __enter__(self):
        return self

    def create_user_bank_account(self, balance):
        self.bank_account = BankAccount(self.user, balance)
        with open('bank.pickle', 'ab') as pkl:
            pickle.dump(self.bank_account, pkl)
        self.result = f'bank account create for user {GREEN}{self.user.full_name}{END} and save successfully'
        self.user.have_bank_account = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.err = exc_val
        if self.err:
            self.err = f'{RED}create bank account fail{END}\n{YELLOW}Hint:{END} {exc_val}'
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
        if exc_val:
            self.err = f'{RED}user register fail{END}\n{YELLOW}Hint:{END} {exc_val}'
        return True
        pass


class WithdrawContextManager:
    def __init__(self, user: User, amount):
        self.user = user
        self.amount = amount
        self.bank_account = None
        self.err = None
        self.result = None

    def __enter__(self):
        return self

    def withdraw(self):
        with open('bank.pickle', 'rb') as bank_file:
            while True:
                try:
                    self.bank_account = pickle.load(bank_file)
                    if self.bank_account.owner.id == self.user.id:
                        self.bank_account.withdraw(self.amount)
                        return
                except EOFError:
                    self.result = f'no bank account for {self.user}'
                    return

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.bank_account.get_balance())
        self.err = exc_val
        if not self.err:
            all_data = read_all_data('bank.pickle')
            with open('bank.pickle', 'wb') as bank_file:
                for idx, bank_account in enumerate(all_data):
                    print(idx, bank_account)
                    if bank_account.owner.id == self.user.id:
                        all_data.remove(bank_account)
                        all_data.insert(idx, self.bank_account)

                for update_bank_account in all_data:
                    pickle.dump(update_bank_account, bank_file)
        else:
            print(exc_val)


