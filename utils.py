import sqlite3
import os


def clear(now=False):
    if not now:
        input('press enter to continue... ')
    os.system('cls') if 'nt' in os.name else os.system('clear')


def get_digit(prompt=""):
    user_input = input(prompt)
    if user_input.isdigit():
        return int(user_input)
    return ''


def database_connector(db_name, conn, cur):
    if conn and cur:
        conn, cur, local_connection = conn, cur, False
    else:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        local_connection = True
    return conn, cur, local_connection