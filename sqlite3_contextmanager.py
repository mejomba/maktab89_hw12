import sqlite3


def create_tables():
    with sqlite3.connect('metro.db') as conn:
        cur = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS user 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name VARCHAR(50), last_name VARCHAR(50),
                 password VARCHAR(64), phone VARCHAR(11), email VARCHAR(64), uuid VARCHAR(64), 
                 is_authenticated BOOLEAN NOT NULL CHECK (is_authenticated IN (0, 1)),
                 have_bank_account BOOLEAN NOT NULL CHECK (have_bank_account IN (0, 1)));
                """
        cur.execute(query)
        query = """CREATE TABLE IF NOT EXISTS user 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name VARCHAR(50), last_name VARCHAR(50),
                         password VARCHAR(64), phone VARCHAR(11), email VARCHAR(64), uuid VARCHAR(64), 
                         is_authenticated BOOLEAN NOT NULL CHECK (is_authenticated IN (0, 1)),
                         have_bank_account BOOLEAN NOT NULL CHECK (have_bank_account IN (0, 1)));
                        """
        conn.commit()


create_tables()
