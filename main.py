import os
from metro import User
from admin import Admin
from custom_contextmanager import CreateUserContextManager


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


def clear():
    os.system('cls') if 'nt' in os.name else os.system('clear')


def var_name(obj, namespace):
    return [name for name in namespace if namespace[name] is obj][0]


def show_menu(menu):
    clear()
    print(f'========== {BLUE}{var_name(menu, globals())}{END} ==========')
    for k, v in menu.items():
        print(f'{k}: {v}')


if __name__ == "__main__":
    while True:
        show_menu(main_menu)
        user_input = int(input('> '))
        if user_input == 1:
            with CreateUserContextManager() as cu:
                cu.create_user('mojtaba', 'aminzadeh', '12345', '0936', 'abc@gmail.com')
            if cu.err:
                print(cu.err)
            elif cu.result:
                print(cu.result)