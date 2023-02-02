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
    with sqlite3.connect('metro.db') as conn:
        cur = conn.cursor()
        query = """INSERT INTO cart_type  
                (cart_type) VALUES (1), (2), (3)
                ;                
                """
        cur.execute(query)

insert_sql()

# create_tables()
def login_to_bank(user_id):
    with sqlite3.connect('metro.db') as conn:
        cur = conn.cursor()
        query = "SELECT * FROm bank_account WHERE owner_id=?"
        data = (user_id,)
        print(cur.execute(query, data).fetchone())
        return cur.execute(query, data).fetchone()


class CreateUserContextManager:
    def __init__(self):
        self.user = None
        self.result = None
        self.err = None
        self.exc_type = None
        self.exc_val = None
        self.conn = None
        self.cur = None

    def __enter__(self):
        return self

    def create_user(self, first_name, last_name, password, phone, email, role):
        self.user = User.register_new_user(first_name, last_name, password, phone, email, role)
        print('after create user')

    def insert_to_database(self):
        if self.user:
            self.user.user_id = None
            self.conn = sqlite3.connect('metro.db')
            self.cur = self.conn.cursor()
            self.user.user_id = User.insert_to_database(self.user, self.cur)
            print(self.user.user_id)
        else:
            raise ValueError('user creation fail')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exc_type = exc_type
        self.exc_val = exc_val
        if exc_val:
            self.user = None
            self.err = f'create user fail\nHint: {exc_val}'
            return True
        elif not exc_val and self.user is not None and self.user.have_bank_account:
            self.result = f'create user {self.user.full_name} successfully'
        elif not self.user.have_bank_account:
            self.err = f"create user fail\nHint: user don't have bank account"


class CreateBankAccountContextManager:
    def __init__(self, user, cur, conn):
        self.user = user
        self.cur = cur
        self.conn = conn
        self.bank = None
        self.result = None
        self.err = None
        self.exc_type = None
        self.exc_val = None

    def __enter__(self):
        return self

    def create_bank_account(self, balance):
        self.bank = BankAccount(owner=self.user, balance=balance)
        print('after create bank')

    def insert_to_database(self):
        BankAccount.insert_to_database(self.bank, self.user, self.cur)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exc_type = exc_type
        self.exc_val = exc_val
        if exc_val:
            self.err = f'create bank account fail\nHint: {self.exc_val}'
            self.cur.execute('ROLLBACK;')
            self.cur.close()
            self.conn.close()
            return True
        elif not exc_val and self.bank is not None:
            self.conn.commit()
            self.user.have_bank_account = True
            self.cur.close()
            self.conn.close()
            self.result = f'create bank account for {self.user.full_name} successfully'


class CreateSuperUserContextManager:
    def __init__(self):
        self.superuser = None
        self.result = None
        self.err = None
        self.exc_type = None
        self.exc_val = None
        self.conn = None
        self.cur = None

    def __enter__(self):
        return self

    def create_superuser(self, first_name, last_name, password, phone, email, role):
        self.superuser = User.register_new_user(first_name, last_name, password, phone, email, role)
        print('after create superuser')

    def insert_to_database(self):
        if self.superuser:
            self.superuser.user_id = None
            self.conn = sqlite3.connect('metro.db')
            self.cur = self.conn.cursor()
            self.superuser.user_id = User.insert_to_database(self.superuser, self.cur)
            print(self.superuser.user_id)
        else:
            raise ValueError('user creation fail')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exc_type = exc_type
        self.exc_val = exc_val
        if exc_val:
            self.superuser = None
            self.err = f'create superuser fail\nHint: {exc_val}'
            return True
        elif not exc_val and self.superuser is not None:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            self.result = f'create user {self.superuser.full_name} successfully'


class WithdrawContextManager:
    def __init__(self):
        self.conn = sqlite3.connect('metro.db')
        self.cur = self.conn.cursor()
        self.err = None
        self.result = None
        self.user = None
        self.balance = None
        self.bank_account_id = None
        self.user_id = None

    def __enter__(self):
        return self

    def withdraw(self, user_id, amount):
        query = """SELECT * FROM bank_account WHERE owner_id=?"""
        self.bank_account_id, self.user_id, self.balance = self.cur.execute(query, (user_id,)).fetchone()
        if self.user_id:
            self.balance = BankAccount.withdraw(self.balance, amount)
            query = """
                    UPDATE bank_account
                    SET balance=?
                    WHERE id=? and owner_id=?
                    """
            self.cur.execute(query, (self.balance, self.bank_account_id, self.user_id))
        else:
            raise TypeError('user not found')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.err = f'withdraw fail\nHint: {exc_val}'
        else:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            self.result = f'withdraw success\n new balance: {self.balance}'
        return True


class DepositContextManager:
    def __init__(self, pk, user_id, balance):
        self.pk = pk
        self.user_id = user_id
        self.balance = balance
        self.conn = sqlite3.connect('metro.db')
        self.cur = self.conn.cursor()
        self.err = None
        self.result = None
        self.user = None
        self.new_balance = None

    def __enter__(self):
        return self

    def deposit(self, amount):
        self.cur.execute("BEGIN TRANSACTION")
        self.new_balance = BankAccount.deposit(self.balance, amount)
        query = """
                    UPDATE bank_account
                    SET balance=?
                    WHERE owner_id=?
                    """
        data = (self.new_balance, self.user_id)
        self.cur.execute(query, data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.cur.execute('ROLLBACK')
            self.cur.close()
            self.conn.close()
            self.err = f'deposit fail\n{exc_val}'
        else:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            self.result = f'deposit success\nyour new balance: {self.new_balance}'
        return True


class BuyTicketContextManager:
    def __init__(self):
        self.conn = sqlite3.connect('metro.db')
        self.cur = self.conn.cursor()
        self.err = None
        self.result = None
        self.user = None

    def __enter__(self):
        return self

    def get_ticket(self, user_id, cart_type):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
