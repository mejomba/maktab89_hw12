import os
from metro import User
from admin import create_super_user
# from custom_contextmanager import (
#     CreateUserContextManager,
#     CreateBankAccountContextManager,
#     SelectUserContextManager,
#     WithdrawContextManager
# )

from sqlite3_contextmanager import (
    CreateUserContextManager as CreateUser,
    CreateBankAccountContextManager as CreateBankAccount,
    WithdrawContextManager,
    DepositContextManager,
    BuyTicketContextManager,
    login_to_bank
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
    3: 'buy ticket for travel',
    4: 'Administrator',
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


def clear():
    os.system('cls') if 'nt' in os.name else os.system('clear')


def var_name(obj, namespace):
    return [name for name in namespace if namespace[name] is obj][0]


def show_menu(menu):
    clear()
    print(f'========== {BLUE}{var_name(menu, globals())}{END} ==========')
    for k, v in menu.items():
        print(f'{k}: {v}')


# def withdraw(user, amount):
#     with WithdrawContextManager(user=user, amount=amount) as w:
#         w.withdraw()


def deposit(user, value):
    pass


def create_regular_user():
    with CreateUser() as cu:
        first_name = input("first name: ")
        last_name = input("last name: ")
        password = input("password: ")
        phone = input("phone: ")
        email = input("email: ")
        cu.create_user(first_name, last_name, password, phone, email)
        with CreateBankAccount(user=cu.user) as cb:
            balance = int(input(f'balance for create {cu.user.full_name} bank account'))
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


def manage_bank_account():
    while True:
        show_menu(bank_menu)
        user_input = int(input("> "))
        if user_input == 1:
            with WithdrawContextManager() as wd:
                amount = int(input('amount for withdraw'))
                wd.withdraw(owner_id, amount)
            if wd.err:
                print(wd.err)
            if wd.result:
                print(wd.result)
        elif user_input == 2:
            amount = int(input('amount for deposit'))
            with DepositContextManager(pk, owner_id, balance) as de:
                de.deposit(amount)
            if de.err:
                print(de.err)
            if de.result:
                print(de.result)
        elif user_input == 0:
            print('exit')
            return
        else:
            print('wrong input')


def buy_ticket():
    user_id = int(input('user id: '))
    cart_type = int(input('cart type: '))
    with BuyTicketContextManager() as buy:
        buy.get_ticket(user_id, cart_type)
    if buy.err:
        print(buy.err)
    if buy.result:
        print(buy.result)


def admin_panel():
    while True:
        show_menu(administrator_menu)
        user_input = int(input('> '))
        if user_input == 1:
            submit_travel()
        elif user_input == 2:
            edit_travel()
        elif user_input == 3:
            create_cart()
        elif user_input == 0:
            print('exit')
            logout_super_user(admin_id)
            return
        else:
            print('wrong input')


if __name__ == "__main__":
    while True:
        show_menu(main_menu)
        user_input = int(input('> '))

        if user_input == 1:
            role = int(input('role: (1: user, 2: admin): '))
            if role == 2:
                create_super_user()
            elif role == 1:
                create_regular_user()

        elif user_input == 2:
            user_id = int(input('user id: '))
            data = login_to_bank(user_id)
            if data:
                pk, owner_id, balance = data
                manage_bank_account()
            else:
                print(f"user {user_id} don't hove bank account")

        elif user_input == 3:
            buy_ticket()

        elif user_input == 4:
            admin_id = int(input('admin id: '))
            admin_password = input('password: ')
            if login_super_user(user_id=admin_id, password=admin_password):
                admin_panel()
        elif user_input == 0:
            print('exit')
            break
        else:
            print('wrong input')
