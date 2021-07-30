import mysql.connector
from mysql.connector import Error
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
        password = login_params[1]
        order_access = login_params[2]
        delivery_access = login_params[3]
        query = f"""insert into users(name, passwords, order_access, delivery_access) values
                        (%s, %s, %s, %s)"""
        values = (name, password, order_access, delivery_access)
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

    def list_all_users(self):
        """
        Get list with users id, name, password, order access delivery access as lists in list
        :param self: object of instance
        :return: list of users i.e. [[1, "admin", "123", 1,1],[2,"admin1","1234",1,0]]
        """
        query = f"""select * from users"""
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query)
            users = cursor.fetchall()
            return users
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            return -2
        except mysql.connector.errors.OperationalError as e:
            print(e)
            return -1

    def delete_user(self, user_id):
        """
        Delete user using ID
        :param user_id: User ID
        :return: True/False
        """
        query = f"DELETE FROM users WHERE id = {user_id}"
        print(query)
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query)
            self.mydb.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except (mysql.connector.errors.IntegrityError, mysql.connector.errors.OperationalError) as e:
            print(e)
            return False

    def modify_user_passwd(self, user_id, new_passwd):
        """
        Upadate password by user id
        :param user_id: User ID
        :param new_passwd: new password
        :return: True/False
        """
        query = "UPDATE users SET passwords = %s WHERE id = %s;"
        values = (new_passwd, user_id)
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, values)
            self.mydb.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except (mysql.connector.errors.IntegrityError, mysql.connector.errors.OperationalError) as e:
            print(e)
            return False

    def verify_user(self, user_data):
        """
            Taking first parameter and validate it with database
            :param self: the object
            :param user_data: list with user data(user_name, password)
            :return: list[1,0]  = [order, delivery]
            """
        username = (user_data[0],)
        try:
            cur = self.mydb.cursor()
            cur.execute("SELECT * FROM users where name= %s", username)

            real_user = cur.fetchone()
            if user_data[1] == real_user[2]:
                return [real_user[3], real_user[4]]
        except TypeError:   # invalid username
            return False
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
        query = f'''insert into products(status,{list_of_parameters}) values (0, {"%s"+", %s"* (len(parameters)-1)})'''
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
        try:
            cur = self.mydb.cursor()
            cur.execute(query, values)
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

    def update_user_access(self, user_id, order, delivery):
        """
        Update user access
        :param id: user id
        :param order: 1/0 (True/False)
        :param delivery: 1/0 (True/False)
        :return: True/False
        """
        query = "UPDATE users SET order_access = %s, delivery_access = %s WHERE id = %s;"
        values = (order, delivery, user_id)
        try:
            cursor = self.mydb.cursor()
            cursor.execute(query, values)
            self.mydb.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except (mysql.connector.errors.IntegrityError, mysql.connector.errors.OperationalError) as e:
            print(e)
            return False

