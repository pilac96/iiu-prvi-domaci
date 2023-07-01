from app import app
import sqlite3


user_db_query = '''
        CREATE TABLE IF NOT EXISTS User (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT NOT NULL,
            Address TEXT NOT NULL,
            PhoneNumber TEXT NOT NULL
        )
    '''

product_db_query = '''
        CREATE TABLE IF NOT EXISTS Product (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL UNIQUE,
            Description TEXT NOT NULL,
            Price DOUBLE NOT NULL,
            Quantity INTEGER NOT NULL
        )
    '''

address_db_query = '''
        CREATE TABLE IF NOT EXISTS Address (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Country TEXT NOT NULL,
            City TEXT NOT NULL,
            Street TEXT NOT NULL UNIQUE,
            PostalCode TEXT NOT NULL
        )
    '''

DATABASE = 'database.db'


def get_db():
    db = getattr(app, '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE, check_same_thread=False)
        app._database = db

        init_db()

    return db


def create_db_table(query):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()


def init_db():
    create_db_table(user_db_query)
    create_db_table(product_db_query)
    create_db_table(address_db_query)
