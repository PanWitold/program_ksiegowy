from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from sqlite3 import Error
import sqlite3
import time
import logging
import sys

import hashlib
import os

databasename = r"database.db"   # path to database file


class DataBase:
    global databasename

    def __init__(self):
        self.database = databasename
        self.conn = None
        self.last_complete_list = []

    def create_connection(self):
        """ create a database connection to the SQLite database
        specified by the self.database
        :return: Connection object or None
        """
        try:
            self.conn = sqlite3.connect(self.database)
        except Error as e:
            print(e)
        return self.conn

    def list_all_users(self):     # id, name
        """Query all users in the table
        :param conn: the Connection object
        :return: list of users with: [id, name, user_name]
        """
        cur = self.conn.cursor()
        cur.execute("SELECT id,name, user_name FROM users")
        rows = cur.fetchall()
        return rows

    def insert_user(self, user_params):
        """
        Adds specified user
        :param user_params: list with(name,user_name, password))
        :return: 1 if ok
                 -1 if broken connection
                 -2 if user exists
        """
        cur = self.conn.cursor()
        salt = os.urandom(32)  # A new salt for this user
        key = hashlib.pbkdf2_hmac('sha256', user_params[2].encode('utf-8'), salt, 100000)
        user_data = list(user_params)
        user_data[2] = key
        user_data.append(salt)
        user_params = tuple(user_data)
        try:
            cur.execute(f'''insert into users(name,user_name, password,seed) values
                        (?,?,?,?)''', user_params)
            if cur.rowcount < 1:    # if not added to db
                logging.warning(f"Błąd przy dodaniu do db")
            else:
                self.conn.commit()

        except sqlite3.OperationalError as e:
            logging.warning(e)
            print("Blad polaczenia z baza danych!!\n", e)
            return -1
        except sqlite3.IntegrityError:
            print("Taki uzytkownik istnieje!")
            return -2
        return 1

    def verify_user(self, user_data):
        """
            Query all rows in the table
            :param self: the object
            :param user_data: list with user data(user_name, password)
            :return: True/False
            """
        username = user_data[0]
        userpass = user_data[1]
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT password,seed "
                        "FROM users where name=:username", {"username": username})
            real_user = cur.fetchone()
            user_real_key = real_user[0]
            seed = real_user[1]
            key = hashlib.pbkdf2_hmac('sha256', userpass.encode('utf-8'), seed, 100000)
        except TypeError:   # invalid username
            return False
        if user_real_key == key:
            return True
        else:
            return False


# Add a user
'''username = 'adkmin'  # The users username
password = 'qwerty'  # The users password

connect = DataBase()
connect.create_connection()

user_data = (username, "Administrator", password)   # when adding (nick, name, passwd)
user_data_to_verify = (username, password)          # when logging

#print(connect.insert_user(user_data))
print(connect.verify_user(user_data_to_verify))'''

#for i in (connect.list_all_users()): print(i)
