import sqlite3
from metro import User, BankAccount


def create_tables():
    with sqlite3.connect('metro.db') as conn:
        cur = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS role 
                (role_id INTEGER PRIMARY KEY AUTOINCREMENT, role_type VARCHAR(50));
                """
        cur.execute(query)

        query = """CREATE TABLE IF NOT EXISTS user 
                (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 first_name VARCHAR(50), 
                 last_name VARCHAR(50),
                 password VARCHAR(64), 
                 phone VARCHAR(11), 
                 email VARCHAR(64), 
                 uuid VARCHAR(64),
                 role_id INTEGER,
                 is_authenticated BOOLEAN NOT NULL CHECK (is_authenticated IN (0, 1)),
                 have_bank_account BOOLEAN NOT NULL CHECK (have_bank_account IN (0, 1)),
                 FOREIGN KEY(role_id) REFERENCES role(role_id)
                 );
                """
        cur.execute(query)

        query = """CREATE TABLE bank_account 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 owner_id INTEGER, 
                 balance INTEGER, 
                 FOREIGN KEY(owner_id) REFERENCES user(user_id)
                );                
                """
        cur.execute(query)

        query = """CREATE TABLE cart_type 
                (cart_type_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                cart_type INTEGER
                );                
                """
        cur.execute(query)

        query = """CREATE TABLE cart 
                (cart_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 credit INTEGER, 
                 expire_date text, 
                 cart_type_id INTEGER, 
                 user_id INTEGER,
                 FOREIGN KEY(cart_type_id) REFERENCES cart_type(cart_type_id),
                 FOREIGN KEY(user_id) REFERENCES user(user_id)
                );                
                """
        cur.execute(query)

        query = """CREATE TABLE travel 
                    (travel_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    price INTEGER, 
                    start_time text, 
                    end_time text,
                    active INTEGER
                    );                
                    """

        cur.execute(query)

        query = """CREATE TABLE user_travel 
                    (user_travel_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    user_id INTEGER, 
                    travel_id INTEGER, 
                    FOREIGN KEY(user_id) REFERENCES user(user_id),
                    FOREIGN KEY(travel_id) REFERENCES travel(travel_id)
                    );                
                    """
        cur.execute(query)


def insert_sql():
    pass


# create_tables()

class CreateUserContextManager:
    def __init__(self):
        self.user = None
        self.bank = None
        self.result = None
        self.err = None

    def __enter__(self):
        return self

    def create_user_transaction(self, first_name, last_name, password, phone, email):
        self.user = User.register_new_user(first_name, last_name, password, phone, email)
        print('after create user')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.user = None
            self.err = f'create user fail\nHint: {exc_val}'
            return True
        elif not exc_val and self.user is not None:
            pass


class CreateBankAccountContextManager:
    def __init__(self, user):
        self.user = user
        self.bank = None
        self.result = None
        self.err = None

    def __enter__(self):
        return self

    def create_bank_account_transaction(self, balance):
        self.bank = BankAccount(owner=self.user, balance=balance)
        print('after create bank')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.err = f'create bank account fail\nHint: {exc_val}'
            return True
        elif not exc_val and self.bank is not None:
            self.result = f'create bank account for {self.user.full_name} successfully'

