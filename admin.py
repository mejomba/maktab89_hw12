from metro import User
from sqlite3_contextmanager import CreateSuperUserContextManager as CreateSuperUser


def create_super_user():
    first_name = input("first name: ")
    last_name = input("last name: ")
    password = input("password: ")
    phone = input("phone: ")
    email = input("email: ")
    with CreateSuperUser() as cu:
        cu.create_superuser(first_name, last_name, password, phone, email, role=2)
        cu.insert_to_database()

    if cu.err:
        print(cu.err)
    elif cu.result:
        print(cu.result)
