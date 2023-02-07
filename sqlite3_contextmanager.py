import sqlite3
from metro import User, BankAccount, Travel, Cart
from custom_exception import (
    WrongPasswordException,
    AccessDeniedException,
    UserNotFound,
    UserCreationFail,
    CreateBankAccountFail,
    CreateSuperUserFail,
)


def create_tables(db_name='metro.db'):
    with sqlite3.connect(db_name) as conn:
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

        query = """CREATE TABLE IF NOT EXISTS bank_account 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 owner_id INTEGER, 
                 balance INTEGER, 
                 FOREIGN KEY(owner_id) REFERENCES user(user_id)
                );                
                """
        cur.execute(query)

        query = """CREATE TABLE IF NOT EXISTS cart_type 
                (cart_type_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                cart_type INTEGER
                );                
                """
        cur.execute(query)

        query = """CREATE TABLE IF NOT EXISTS cart 
                (cart_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 credit INTEGER, 
                 expire_date text, 
                 cart_type_id INTEGER UNIQUE, 
                 FOREIGN KEY(cart_type_id) REFERENCES cart_type(cart_type_id)
                );                
                """
        cur.execute(query)

        query = """CREATE TABLE IF NOT EXISTS user_cart
                    (user_cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    cart_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES user(user_id),
                    FOREIGN KEY(cart_id) REFERENCES cart(cart_id)
                    );
                    """
        cur.execute(query)

        query = """CREATE TABLE IF NOT EXISTS travel 
                    (travel_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    price INTEGER, 
                    start_time text, 
                    end_time text,
                    active INTEGER
                    );                
                    """

        cur.execute(query)

        query = """CREATE TABLE IF NOT EXISTS user_travel 
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

# insert_sql()

# create_tables()


def login_to_bank(user_id):
    with sqlite3.connect('metro.db') as conn:
        cur = conn.cursor()
        query = "SELECT * FROm bank_account WHERE owner_id=?"
        data = (user_id,)
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
        self.local_connection = None

    def __enter__(self):
        return self

    def create_user(self):
        first_name = input("first name: ")
        last_name = input("last name: ")
        password = input("password: ")
        phone = input("phone: ")
        email = input("email: ")
        self.user = User.register_new_user(first_name, last_name, password, phone, email, 1)

        if self.user:
            self.user.user_id = None
            self.conn = sqlite3.connect('metro.db')
            self.cur = self.conn.cursor()
            self.local_connection = True
            self.user.user_id = User.insert_to_database(self.user, self.cur)
        else:
            raise UserCreationFail('user creation fail')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val and self.local_connection:
            self.user = None
            self.err = f'create user fail\nHint: {exc_val}'
            self.cur.execute('ROLLBACK')
            self.cur.close()
            self.conn.close()
        elif exc_val and not self.local_connection:
            self.err = f'create user fail\nHint: {exc_val}'
        elif not exc_val and self.user is not None and self.user.have_bank_account and self.local_connection:
            self.conn.commit()
            self.cur.close()
            self.conn.commit()
            self.result = f'create user {self.user.full_name} successfully ID: {self.user.user_id}'
        elif not self.user.have_bank_account:
            self.err = f"create user fail\nHint: user don't have bank account"
        return True


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
        self.local_connection = None

    def __enter__(self):
        return self

    def create_bank_account(self, balance):
        self.bank = BankAccount(owner=self.user, balance=balance)
        if self.bank:
            BankAccount.insert_to_database(self.bank, self.user, self.cur)
        else:
            raise CreateBankAccountFail('create bank account fail')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.err = f'create bank account fail\nHint: {self.exc_val}'
            return True
        elif not exc_val and self.bank is not None:
            self.user.have_bank_account = True
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
        if self.superuser:
            self.superuser.user_id = None
            self.conn = sqlite3.connect('metro.db')
            self.cur = self.conn.cursor()
            self.superuser.user_id = User.insert_to_database(self.superuser, self.cur)
        else:
            raise CreateSuperUserFail('superuser creation fail')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exc_type = exc_type
        self.exc_val = exc_val
        if exc_val:
            self.superuser = None
            self.err = f'create superuser fail\nHint: {exc_val}'
        elif not exc_val and self.superuser is not None:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            self.result = f'create user {self.superuser.full_name} successfully. id: {self.superuser.user_id}'
        return True


class WithdrawContextManager:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.local_connection = None
        self.err = None
        self.result = None
        self.user = None
        self.balance = None
        self.bank_account_id = None
        self.user_id = None

    def __enter__(self):
        return self

    def withdraw(self, user_id, amount, conn=None, cur=None):
        if conn and cur:
            self.conn = conn
            self.cur = cur
            self.local_connection = False
        else:
            self.conn = sqlite3.connect('metro.db')
            self.cur = self.conn.cursor()
            self.local_connection = True

        query = """SELECT * FROM bank_account WHERE owner_id=?"""
        self.bank_account_id, self.user_id, self.balance = self.cur.execute(query, (user_id,)).fetchone()
        if self.user_id:
            self.balance = BankAccount.withdraw(self.balance, amount)
            query = """
                    UPDATE bank_account
                    SET balance=?
                    WHERE id=? and owner_id=?
                    """
            data = (self.balance, self.bank_account_id, self.user_id)
            self.cur.execute(query, data)
        else:
            raise TypeError('user not found')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.err = f'withdraw fail\nHint: {exc_val}'
            if self.local_connection:
                self.cur.close()
                self.conn.close()
        elif self.local_connection:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            self.result = f'withdraw success\n new balance: {self.balance}'
        else:
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
        self.user_balance = None

    def __enter__(self):
        return self

    def get_ticket(self, user_id, cart_type):
        cart_price = None
        self.cur.execute("BEGIN TRANSACTION")
        query = """SELECT credit FROM cart
                    WHERE cart_type_id=?
                """
        data = (cart_type,)
        cart_price = self.cur.execute(query, data).fetchone()[0]

        with WithdrawContextManager() as wd:
            wd.withdraw(user_id, amount=cart_price, conn=self.conn, cur=self.cur)
        if wd.err:
            print(wd.err)
            raise Exception('TODO: create buy ticket exception')
        if wd.result:
            print(wd.result)
        query = """INSERT INTO user_cart (user_id, cart_id)
                    VALUES(?,?)
                """
        data = user_id, cart_type
        self.cur.execute(query, data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.cur.execute("ROLLBACK")
            self.err = f'buy ticket fail\nHint: {exc_val}'
        else:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            self.result = f'buy ticket'
        return True


class AuthContextManager:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.local_connection = None
        self.err = None
        self.result = None
        self.__first_name = None
        self.__last_name = None
        self.__is_authenticated = None

    def __enter__(self):
        return self

    def login(self, user_id, password, conn=None, cur=None):
        if conn and cur:
            self.conn = conn
            self.cur = cur
            self.local_connection = False
        else:
            self.conn = sqlite3.connect('metro.db')
            self.cur = self.conn.cursor()
            self.local_connection = True

        query = """
                SELECT first_name, last_name, password, role_id, is_authenticated FROM user
                WHERE user_id=?
        """
        data = (user_id,)

        if self.local_connection:
            self.cur.execute("BEGIN TRANSACTION")

        record = self.cur.execute(query, data).fetchone()
        if record:
            self.__first_name, self.__last_name, hash_password, role_id, self.__is_authenticated = record
        else:
            raise UserNotFound('user not found')

        if role_id != 2:
            raise AccessDeniedException(f'user_id {user_id} not admin')
        if User.login(password, hash_password):
            is_authenticated = 1
            query = """
                    UPDATE user
                    SET is_authenticated=?
                    WHERE user_id=?
            """
            data = (is_authenticated, user_id)
            self.cur.execute(query, data)
        else:
            raise WrongPasswordException('wrong password')

    def logout(self, user_id, conn=None, cur=None):
        if conn and cur:
            self.conn = conn
            self.cur = cur
            self.local_connection = False
        else:
            self.conn = sqlite3.connect('metro.db')
            self.cur = self.conn.cursor()
            self.local_connection = True
        query = """
                UPDATE user
                SET is_authenticated=0
                WHERE user_id=?
                """
        data = (user_id,)
        self.cur.execute(query, data)
        self.__is_authenticated = 0

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.err = f'login fail\nHint: {exc_val}'
            if self.local_connection:
                self.cur.execute("ROLLBACK")
                self.cur.close()
                self.conn.close()
        elif self.local_connection:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            if self.__is_authenticated:
                self.result = f'login success\n welcome: {self.__first_name} {self.__last_name}'
            else:
                self.result = f'logout success'
        else:
            if self.__is_authenticated:
                self.result = f'login success\n welcome: {self.__first_name} {self.__last_name}'
            else:
                self.result = f'logout success'

        return True


class TravelContextManager:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.local_connection = None
        self.err = None
        self.result = None

    def __enter__(self):
        return self

    def add_travel(self, price: int, start_time: str, end_time: str, conn=None, cur=None):
        if conn and cur:
            self.conn = conn
            self.cur = cur
            self.local_connection = False
        else:
            self.conn = sqlite3.connect('metro.db')
            self.cur = self.conn.cursor()
            self.local_connection = True

        query = """
                INSERT INTO travel (price, start_time, end_time, active)
                VALUES(?,?,?,?);
                """

        data = Travel.valid_data((start_time, end_time), price)

        # data = (price, start_time, end_time, Travel.is_active(end_time))
        self.cur.execute(query, data)

    def edit_travel(self):
        self.__show_travel()
        travel_number = int(input('travel number for edit or delete: '))
        while True:
            user_input = int(input(f'option(1: update travel {travel_number},   2: delete travel {travel_number} 0:exit)'))
            if user_input == 1:
                query = """
                        SELECT * from travel
                        WHERE travel_id=?
                        """
                data = (travel_number,)
                record = self.cur.execute(query, data).fetchone()
                if record:
                    travel_id, price, start_time, end_time, active = record

                    new_price = int(input('new price (press enter for leaving): '))
                    new_start_time = input('new start_time (press enter for leaving): ')
                    new_end_time = input('new end_time (press enter for leaving): ')

                    if new_price is None:
                        new_price = price
                    if new_start_time is None:
                        new_start_time = start_time
                    if new_end_time is None:
                        new_end_time = end_time

                    query = """
                            UPDATE travel
                            set price=?, start_time=?, end_time=?, active=?
                            WHERE travel_id=?
                            """
                    price, start_time, end_time, active = Travel.valid_data((new_start_time, new_end_time), new_price)
                    data = (price, start_time, end_time, active, travel_id)
                    self.cur.execute(query, data)
                    print(f'UPDATE SUCCESS')
                else:
                    print(f'travel {travel_number} not found')
            elif user_input == 2:
                query = """
                        DELETE FROM travel
                        WHERE travel_id=?
                        """
                data = (travel_number,)
                self.cur.execute(query, data)
                print(f'DELETE SUCCESS')
            elif user_input == 0:
                break
            else:
                print('wrong input')
            user_input = input(f'option(0:exit, press any key to continue)')
            if user_input == '0':
                break
            travel_number = int(input('travel number for edit or delete: '))

    def __show_travel(self):
        if self.conn is None and self.cur is None:
            self.conn = sqlite3.connect('metro.db')
            self.cur = self.conn.cursor()
            self.local_connection = True

        query = """
                SELECT * FROM travel;
                """
        records = self.cur.execute(query).fetchall()
        print(f'number    price    start_time      end_time    active')
        for record in records:
            travel_id, price, start_time, end_time, active = record
            print(f'{travel_id:<9} {price:<8} {start_time:<15} {end_time:<10} {active:>2}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.err = f'travel submit fail\nHint: {exc_val}'
            if self.local_connection:
                self.cur.close()
                self.conn.close()
        elif self.local_connection:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            if self.cur.lastrowid:
                self.result = f'travel submit success\n travel id: {self.cur.lastrowid}'
            else:
                self.result = f'process success'
        else:
            self.result = f'travel submit success\n travel id: {self.cur.lastrowid}'
        return True


class CartContextManager:
    def __init__(self):
        self.cart = None
        self.conn = None
        self.cur = None
        self.local_connection = None
        self.result = None
        self.err = None

    def __enter__(self):
        return self

    def create_cart(self, conn=None, cur=None):
        cart_type = int(input("cart_type(1,2,3): "))
        cart_price = input("cart price: ")
        if cart_type == 3:
            cart_expire_period = input('expire period: ')
        else:
            cart_expire_period = None
        self.cart = Cart.create_cart(cart_type, cart_price, cart_expire_period)

        if conn and cur:
            self.conn = conn
            self.cur = cur
            self.local_connection = False
        else:
            self.conn = sqlite3.connect('metro.db')
            self.cur = self.conn.cursor()
            self.local_connection = True

        query = """
                INSERT INTO cart (credit, expire_date, cart_type_id)
                VALUES(?,?,?);
                """
        data = (self.cart.credit, self.cart.expire_date, self.cart.cart_type)
        self.cur.execute(query, data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.err = f'cart submit fail\nHint: {exc_val}'
            if self.local_connection:
                self.cur.close()
                self.conn.close()
        elif self.local_connection:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            if self.cur.lastrowid:
                self.result = f'cart submit success\n cart id: {self.cur.lastrowid}'
            else:
                self.result = f'process success'
        else:
            self.result = f'cart submit success\n cart id: {self.cur.lastrowid}'
        return True
