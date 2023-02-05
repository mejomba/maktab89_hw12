from metro import User
from sqlite3_contextmanager import (
    CreateSuperUserContextManager as CreateSuperUser,
    AuthContextManager as Auth,
    TravelContextManager as Travel,
    CartContextManager as Cart,
)
from metro import User


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


def login_super_user(user_id, password):
    with Auth() as login:
        login.login(user_id, password)
    if login.err:
        print(login.err)
    if login.result:
        print(login.result)
        return True


def submit_travel():
    price = int(input("price: "))
    start_time = input('start_time (yyyy/mm/dd): ')
    end_time = input('end_time (yyyy/mm/dd): ')
    with Travel() as travel:
        travel.add_travel(price, start_time, end_time)
    if travel.err:
        print(travel.err)
    if travel.result:
        print(travel.result)


def edit_travel():
    with Travel() as travel:
        travel.edit_travel()
    if travel.err:
        print(travel.err)
    if travel.result:
        print(travel.result)


def logout_super_user(user_id):
    with Auth() as logout:
        logout.logout(user_id)
    if logout.err:
        print(logout.err)
    if logout.result:
        print(logout.result)


def create_cart():
    # todo add unique constraint to cart_type_id
    with Cart() as cart:
        cart.create_cart()