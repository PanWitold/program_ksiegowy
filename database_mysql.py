import mysql.connector
from mysql.connector import connect, Error
import hashlib
import os


class DataBase:

    def __init__(self):
        self.db_host = "192.168.0.171"
        self.db_user = "B5uc6E"
        self.db_password = "JQqsvCk8VT"
        self.db_database = "products"
        self.conn = None
        self.last_complete_list = []

    def create_connection(self):
        """ create a database connection to the SQLite database
        specified by the self.database
        :return: Connection object or None
        """
        try:
            connection = mysql.connector.connect(
                                                host=self.db_host,
                                                user=self.db_user,
                                                password=self.db_password,
                                                database=self.db_database)
            if connection.is_connected():
                return self.conn
        except Error as e:
            print(e)

    def add_user(self, login_params):
        """
        Adds specified user
        :param login_params: list (name, password, order_access, delivery_access))
        :return: 1 if ok
                 -1 if broken connection
                 -2 if user exists
        """
        name = login_params[0]
        salt = os.urandom(32)  # A new salt for this user
        password = hashlib.pbkdf2_hmac('sha256', login_params[1].encode('utf-8'), salt, 100000)
        order_access = login_params[2]
        delivery_access = login_params[3]
        query = f"""insert into users(name, password, seed, order_access, delivery_access) values
                        ({name}, {password}, {salt}, {order_access}, {delivery_access}"""
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.conn.commit()


username = "admin"
password = "qwerty"
user_params = (username, password, 1, 0)   # when adding (login, passwd, order_access, delivery_access)

#salt = os.urandom(32)  # A new salt for this user
#key = hashlib.pbkdf2_hmac('sha256', user_params[1].encode('utf-8'), salt, 100000)

db = DataBase()
print(db.create_connection())
db.add_user(login_params)

#print(f"salt: len:{len(salt)} text:{salt}\npasswd: len:{len(key)} text: {key}")