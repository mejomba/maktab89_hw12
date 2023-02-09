import os
from utils import get_digit, clear
from admin import create_super_user

from sqlite3_contextmanager import (
    CreateUserContextManager as CreateUser,
    CreateBankAccountContextManager as CreateBankAccount,
    WithdrawContextManager,
    DepositContextManager,
    BuyTicketContextManager,
    TravelContextManager,
    login_to_bank,
    create_tables
)
from admin import (
    login_super_user,
    submit_travel,
    edit_travel,
    logout_super_user,
    create_cart,
)

RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"

main_menu = {
    1: 'register new user',
    2: 'manage bank account',
    3: 'buy ticket',
    4: 'Administrator',
    5: 'select travel',
    0: 'exit'
}
administrator_menu = {
    1: 'submit travel',
    2: 'edit travel',
    3: 'add cart',
    0: 'exit'
}

bank_menu = {
    1: 'withdraw',
    2: 'deposit',
    0: 'exit'
}


def var_name(obj, namespace):
    return [name for name in namespace if namespace[name] is obj][0]


def show_menu(menu):
    print(f'========== {BLUE}{var_name(menu, globals())}{END} ==========')
    for k, v in menu.items():
        print(f'{k}: {v}')


def create_regular_user():
    with CreateUser() as cu:
        first_name = input("first name: ")
        last_name = input("last name: ")
        password = input("password: ")
        phone = input("phone: ")
        email = input("email: ")
        cu.create_user(first_name, last_name, password, phone, email)
        with CreateBankAccount(user=cu.user) as cb:
            balance = get_digit(f'balance for create {cu.user.full_name} bank account: ')
            cb.create_bank_account(balance, conn=cu.conn, cur=cu.cur)
        if cb.err:
            print(cb.err)
        elif cb.result:
            print(cb.result)
    if cu.err:
        print(cu.err)
    elif cu.result:
        print(cu.result)
    if cu.user and cb.bank:
        print('Done')
    # clear()


def manage_bank_account(pk, owner_id, balance):
    while True:
        show_menu(bank_menu)
        user_input = get_digit('> ')
        if user_input == 1:
            with WithdrawContextManager() as wd:
                amount = get_digit('amount for withdraw: ')
                wd.withdraw(owner_id, amount)
            if wd.err:
                print(wd.err)
            if wd.result:
                print(wd.result)
            balance = wd.balance
            clear()
        elif user_input == 2:
            amount = get_digit('amount for deposit: ')
            with DepositContextManager(pk, owner_id, balance) as de:
                de.deposit(amount)
            if de.err:
                print(de.err)
            if de.result:
                print(de.result)
            balance = de.new_balance
            clear()
        elif user_input == 0:
            print('exit')
            return
        else:
            print('wrong input')
            clear()


def buy_ticket():
    user_id = get_digit('user_id: ')
    cart_type = get_digit('cart type: ')
    with BuyTicketContextManager() as buy:
        clear(True)
        buy.get_ticket(user_id, cart_type)
    if buy.err:
        print(buy.err)
    if buy.result:
        print(buy.result)
    # clear()


def admin_panel():
    while True:
        # clear(True)
        show_menu(administrator_menu)
        user_input = get_digit('> ')
        if user_input == 1:
            submit_travel()
            clear()
        elif user_input == 2:
            edit_travel()
            clear()
        elif user_input == 3:
            create_cart()
            clear()
        elif user_input == 0:
            print('exit')
            logout_super_user(admin_id)
            return
        else:
            print('wrong input')
            clear()
        # clear()


def select_travel(user_id, user_cart_id):
    with TravelContextManager() as tr:
        # clear(now=True)
        tr.select_travel(user_id, user_cart_id)
    if tr.err:
        print(tr.err)
    if tr.result:
        print(tr.result)
    # clear()


if __name__ == "__main__":
    create_tables()
    while True:
        show_menu(main_menu)
        user_input = get_digit("> ")

        if user_input == 1:  # register new user
            clear(True)
            role = get_digit('role: (1: user, 2: admin): ')
            if role == 2:
                create_super_user()
                clear()
            elif role == 1:
                create_regular_user()
                clear()
            else:
                print('wrong input')
                clear()

        elif user_input == 2:  # manage bank account
            if user_id := get_digit('user_id: '):
                if data := login_to_bank(user_id):
                    manage_bank_account(*data)
                    clear(True)
                else:
                    print(f"user {user_id} don't hove bank account")
                    clear()
            else:
                print('wrong input')
                clear()

        elif user_input == 3:  # buy ticket for travel
            buy_ticket()
            clear()

        elif user_input == 4:  # administrator
            admin_id = get_digit('admin id:')
            admin_password = input('password: ')
            if login_super_user(user_id=admin_id, password=admin_password):
                admin_panel()
                clear()

        elif user_input == 5:
            user_id = get_digit('user_id: ')
            user_cart_id = get_digit('your cart/ticket id: ')
            select_travel(user_id, user_cart_id)
            clear()

        elif user_input == 0:  # exit
            print('exit')
            break
        else:
            print('wrong input')
