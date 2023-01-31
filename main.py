import os
from metro import User
from admin import Admin
from custom_contextmanager import (
    CreateUserContextManager,
    CreateBankAccountContextManager,
    SelectUserContextManager,
    WithdrawContextManager
)

from sqlite3_contextmanager import (
    CreateUserContextManager as CreateUser,
    CreateBankAccountContextManager as CreateBankAccount,
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


def withdraw(user, amount):
    with WithdrawContextManager(user=user, amount=amount) as w:
        w.withdraw()


def deposit(user, value):
    pass


if __name__ == "__main__":
    # while True:
    #     show_menu(main_menu)
    #     user_input = int(input('> '))
    #
    #     if user_input == 1:
    #         with CreateUserContextManager() as cu:
    #             first_name = input("first name: ")
    #             last_name = input("last name: ")
    #             password = input("password: ")
    #             phone = input("phone: ")
    #             email = input("email: ")
    #             cu.create_user(first_name, last_name, password, phone, email)
    #             if cu.user:
    #                 with CreateBankAccountContextManager(cu.user) as ba:
    #                     user_input = int(input(f"balance for {GREEN}{cu.user.full_name}{END} bank account: "))
    #                     ba.create_user_bank_account(user_input)
    #                 if ba.err:
    #                     print(ba.err)
    #                 elif ba.result:
    #                     print(ba.result)
    #         if cu.err:
    #             print(cu.err)
    #         elif cu.result:
    #             print(cu.result)
    #
    #     elif user_input == 2:
    #         with SelectUserContextManager() as su:
    #             user_id = int(input('user id: '))
    #             su.select_user(user_id=user_id)
    #             print(su.result)
    #             if su.user:
    #                 input_password = input('your password: ')
    #                 su.login_user(input_password)
    #                 print(su.result)
    #
    #                 if su.user.is_authenticated:
    #                     while True:
    #                         show_menu(bank_menu)
    #                         user_input = int(input('> '))
    #                         if user_input == 1:
    #                             # ToDo "withdraw action"
    #                             amount = int(input('balance for withdraw: '))
    #                             withdraw(su.user, amount=amount)
    #                             print('withdraw')
    #                         elif user_input == 2:
    #                             # ToDo "deposit action"
    #                             balance = int(input('balance for deposit: '))
    #                             deposit(su.user, balance)
    #                             print('deposit')
    #                         elif user_input == 0:
    #                             # todo "exit"
    #                             print('exit')
    #                             break
    #                         else:
    #                             # todo "wrong input"
    #                             print('wrong input')
    show_menu(main_menu)
    user_input = int(input('> '))
    if user_input == 1:
        with CreateUser() as cu:
            first_name = input("first name: ")
            last_name = input("last name: ")
            password = input("password: ")
            phone = input("phone: ")
            email = input("email: ")
            role = int(input('role: (1: user, 2: admin): '))
            cu.create_user(first_name, last_name, password, phone, email, role)
            with CreateBankAccount(user=cu.user) as cb:
                balance = int(input(f'balance for create {cu.user.full_name} bank account'))
                cb.create_bank_account(balance)
            if cb.err:
                print(cb.err)
            elif cb.result:
                print(cb.result)
        if cu.err:
            print(cu.err)
        elif cu.result:
            print(cu.result)
        if cu.user and cb.bank:
            print('insert into data base.')