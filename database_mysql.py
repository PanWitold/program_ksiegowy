import mysql.connector
from mysql.connector import Error
import hashlib
import os
import passwords


class DataBase:
    def __init__(self):
        self.db_host = passwords.db_host
        self.db_user = passwords.db_user
        self.db_password = passwords.db_password
        self.db_database = passwords.db_database
        self.mydb = None
        self.last_complete_list = []

    def create_connection(self):
        """ create a database connection to the SQLite database
        specified by the self.database
        :return: Connection object or None
        """
        #todo do usuniecia
        return True
        try:
            self.mydb = mysql.connector.connect(host=self.db_host,
                                                user=self.db_user,
                                                password=self.db_password,
                                                database=self.db_database,
                                                connection_timeout=2)
            if self.mydb.is_connected():
                return self.mydb
        except Error as e:
            print(e)
            return None

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
                        (%s, %s, %s, %s, %s)"""
        values = (name, password, salt, order_access, delivery_access)
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, values)
            self.mydb.commit()
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            return -2
        except mysql.connector.errors.OperationalError as e:
            print(e)
            return -1
        return 1

    def verify_user(self, user_data):
        """
            Taking first parameter and validate it with database
            :param self: the object
            :param user_data: list with user data(user_name, password)
            :return: True/False
            """
        #todo usuniecie
        return [1, 1]

        username = (user_data[0],)
        userpass = user_data[1]
        try:
            cur = self.mydb.cursor()
            cur.execute("SELECT password,seed  FROM users where name= %s and delivery_access = 1;", username)

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

    def add_order(self, orderer, code, info, value, note):
        """
        Add an order to database
        :param self: the object
        :param orderer: orderer
        :param code: code
        :param info: info
        :param value: how many iterations of adding
        :param note: note
        :return: True/False
        """
        list_of_parameters = ""  # as str
        list_of_products = []
        parameters = []
        if len(orderer) >= 1:
            list_of_parameters += "orderer"
            parameters.append(orderer)
        if len(code) >= 1:
            list_of_parameters += ", code"
            parameters.append(code)
        if len(info) >= 1:
            list_of_parameters += ", info"
            parameters.append(info)
        if len(note) >= 1:
            list_of_parameters += ", note"
            parameters.append(note)
        print(list_of_products, list_of_parameters, sep="\n")
        query = f'''insert into products(status,{list_of_parameters}) values (0, {"%s"+", %s"* (len(parameters)-1)})'''
        print(query)
        for i in range(0, int(value)):
            list_of_products.append(tuple(parameters))
        try:
            cur = self.mydb.cursor()
            if int(value) > 1:
                cur.executemany(query, list_of_products)
            else:
                cur.execute(query, list_of_products[0])
            if cur.rowcount < 1:  # if not added to db
                print(f"Błąd przy dodaniu do db")
                return False
            else:
                self.mydb.commit()
        except ValueError as e:
            print(e)
            return False
        except mysql.connector.errors.OperationalError as e:
            print(e)
            print("Blad polaczenia z baza danych!!\n", e)
            return False
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            return False
        return True

    def search_product(self, product_code):
        """
        Used to search oldest product pointed by code
        :param self: the object
        :param product_code: product ID in database
        :return: product: code, date_ordered, orderer, note, id
        :return: False if error
        """
        query = (f'select code, date_ordered, orderer, note, id from products where code = %s and date_delivered is NULL order by date_ordered asc limit 1;')
        cur = self.mydb.cursor()
        try:
            cur.execute(query, (product_code,))

            val = list(cur.fetchone())
            val[1] = val[1].strftime('%Y-%m-%d %H:%M:%S')
            val = tuple(val)
            cur.close()
            return val
        except mysql.connector.errors.OperationalError as e:
            print(e)
            print("Blad polaczenia z baza danych!!\n", e)
            return False
        except TypeError as e:
            print(e, "Brak takiego produktu!")
            return False

    def update_order(self, product_id, nr_delivery):
        """
        Used to search oldest product pointed by code
        :param self: the object
        :param product_code: product ID in database
        :return: product: code, date_ordered, orderer, note, id
        :return: False if error
        """
        query = 'UPDATE products set date_delivered=CURRENT_TIMESTAMP, nr_delivery = %s where id = %s;'
        values = (nr_delivery, product_id)
        print(query, values, sep="\n")
        try:
            cur = self.mydb.cursor()
            cur.execute(query, values)
            print(cur)
            print("rowcount: ", cur.rowcount)
            self.mydb.commit()
        except mysql.connector.errors.OperationalError as e:
            print(e)
            return False
        if cur.rowcount < 1:  # if not added to db
            print("Wierszy: ", cur.rowcount)
            print(f"Błąd przy dodaniu do db")
            return False
        else:
            print("zaktualizowano")
            return True
