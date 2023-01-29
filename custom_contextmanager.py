from metro import User

RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
END = "\033[0m"


class CreateUserContextManager:
    def __init__(self):
        self.user = None
        self.err = None

    def __enter__(self):
        return self

    def create_user(self, first_name, last_name, password, phone, email):
        self.user = User.register_new_user(first_name, last_name, password, phone, email)
        print('after user create')


    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.err = f'{RED}user register fail{END}\n{YELLOW}Hint:{END} {exc_val}'
        return True
