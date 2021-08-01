import database_mysql as Database
import os
import datetime
import xlsxwriter
import csv
import passwords

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from templates.dodawanie_kont import add_user
from templates.dostawy import main_window, ordered_table
from templates.zamowienia import main, order
from templates import login, moduly

dir_output_files_delivery = passwords.dir_dostawy    # directory will be created if no exists
dir_output_files_orders = passwords.dir_zamowienia


def csv_writer(filename, list_params):
    headers = ["kod", "opis", "sztuk", "notatka"]
    add_headers = True
    if os.path.isfile(filename):
        add_headers = False
    with open(filename, 'a', newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        if add_headers:
            csvwriter.writerow(headers)
        csvwriter.writerow(list_params)


class LoginWindow(QtWidgets.QMainWindow, login.Ui_LOGIN):
    logged = QtCore.pyqtSignal()
    order = QtCore.pyqtSignal()
    delivery = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setupUi(self)
        self.pushButton.clicked.connect(self.verify_user)
        self.input_login.textChanged.connect(self.statusbar.clearMessage)
        self.input_passwd.textChanged.connect(self.statusbar.clearMessage)

    def verify_user(self):
        user_login = self.input_login.text()
        user_password = str(self.input_passwd.text())
        db = Database.DataBase()
        if db.create_connection() is None:
            self.showDialog("Brak połączenia z serwerem!", "Wystąpił błąd przy próbie połączenia z serwerem.\n"
                                                           "Sprawdź połączenie internetowe lub spróbuj ponownie później."
                                                           "\nJeżeli to nie przyniesie efektów: skontaktuj się z PCLAND")
            return False
        login_auth = (user_login, user_password)
        db_return = db.verify_user(login_auth)

        if db_return == [1, 1]:
            self.logged.emit()
            self.close()
        elif db_return == [0, 1]:
            self.delivery.emit()
            self.close()
        elif db_return == [1, 0]:
            self.order.emit()
            self.close()
        elif db_return == [0, 0]:
            self.showDialog("Brak uprawnień!", "Na koncie nie ma uprawnień do logowania!")
        else:
            self.statusbar.showMessage("Błędny login/hasło")
            self.showDialog("Błąd!", "Błędny login/hasło!")

    def showDialog(self, title, msg):
        QMessageBox.critical(self, title, msg)


class ModuleWindow(QtWidgets.QMainWindow, moduly.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ModuleWindow, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setupUi(self)


class MainWindowDelivery(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    ordered = QtCore.pyqtSignal()
    exit = QtCore.pyqtSignal()
    product = ""
    delivery = ""
    product_list = []

    def __init__(self, parent=None):
        super(MainWindowDelivery, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.pushButton.clicked.connect(self.order_product)
        self.pushButton.clicked.connect(self.product_code.clear)
        self.pushButton_2.clicked.connect(self.end)

    def order_product(self):
        self.product = self.product_code.text()
        self.delivery = self.delivery_nr.text()

        if self.delivery == "":
            self.show_message("Dostawa.", "Wprowadź numer dostawy!")
        elif self.product == "":
            self.show_message("Brak numeru", "Wprowadź kod produktu!")
        else:
            db = Database.DataBase()
            db.create_connection()
            self.product_list = db.search_product(self.product)
            try:
                if len(self.product_list) > 1:
                    self.ordered.emit()
                else:
                    self.show_message("Brak produktu", "Brak produktu o podanym kodzie!")
            except TypeError:
                self.show_message("Brak produktu", "Brak produktu o podanym kodzie!")

    def end(self):
        self.exit.emit()

    def show_message(self, title, msg):
        QMessageBox.warning(self, title, msg)


class OrderedTable(QtWidgets.QMainWindow, ordered_table.Ui_MainWindow):
    ordered = QtCore.pyqtSignal()
    gen_xls = QtCore.pyqtSignal()   # and end work all application
    product_id = ""
    nr_delivery = ""

    def __init__(self, parent):
        super(OrderedTable, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.pushButton.clicked.connect(self.update_orderer)   # zatwierdz
        self.pushButton_2.clicked.connect(self.close)          # usuń
        self.pushButton_3.clicked.connect(self.end_ordered)    # koniec - zamknij wszystkie okna

    def add_table(self, table_list):
        for i in range(0, len(table_list)-1):
            self.tableWidget.setRowCount(1)
            if str(table_list[i]) == "None":
                self.tableWidget.setItem(0, i, QtWidgets.QTableWidgetItem(""))
            else:
                self.tableWidget.setItem(0, i, QtWidgets.QTableWidgetItem(str(table_list[i])))
            self.tableWidget.resizeColumnsToContents()

    def update_orderer(self):
        db = Database.DataBase()
        db.create_connection()
        if db.update_order(self.product_id, self.nr_delivery):
            self.show_about_message("Powodzenie", "Produkt przypisano do zamówienia")
            self.ordered.emit()
            self.close()
        else:
            self.show_warning_message("Niepowodzenie", "Wystąpił błąd przy aktualizacji bazy danych")

    def end_ordered(self):
        self.gen_xls.emit()

    def show_about_message(self, title, msg):
        QMessageBox.about(self, title, msg)

    def show_warning_message(self, title, msg):
        QMessageBox.warning(self, title, msg)


class MainWindowUsers(QtWidgets.QMainWindow, add_user.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindowUsers, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setupUi(self)
        self.submit.clicked.connect(self.submited)

    def submited(self):
        password1 = self.passwd.text()
        password2 = self.con_passwd.text()
        name = self.login.text()
        if password1 != password2:
            self.show_warning("Niezgodność haseł", "Hasła się nie zgadzają")
            self.passwd.clear()
            self.con_passwd.clear()
            self.passwd.setFocus()
            return False

        db = Database.DataBase()
        db.create_connection()
        ret = 0
        if self.both.isChecked():
            user_args = (name, password1, 1, 1)
            ret = db.add_user(user_args)

        elif self.order.isChecked():
            user_args = (name, password1, 1, 0)
            ret = db.add_user(user_args)

        elif self.delivery.isChecked():
            user_args = (name, password1, 0, 1)
            ret = db.add_user(user_args)

        if ret == 1:
            self.show_warning("Dodano", f"Użytkownik {name} został dodany.")
        elif ret == -2:
            self.show_warning("Błąd", f"Użytkownik {name} istnieje.\nWybierz inną nazwę.")
        elif ret == -1:
            self.show_warning("Błąd", "Przekroczono czas połączenia, spróbuj ponownie.")

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)


class MainWindowOrder(QtWidgets.QMainWindow, main.Ui_MainWindow):
    order_table = []
    ordered = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindowOrder, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setupUi(self)
        self.order.clicked.connect(self.order_product)

    def order_product(self):
        orderer = self.username.text()
        code = self.code.text()
        info = self.info.text()
        how_many = self.val.text()
        note = self.note.text()
        product_table = [orderer, code, info, how_many, note]
        counter = 0
        try:
            for i in product_table:  # verify input text
                if i != '':
                    counter += 1
            if int(how_many) == 0 or how_many == "":  # number of ordered product cannot be at 0
                self.show_warning("Błąd!", "Ilość zamawianego towaru musi być > 0")

            elif counter > 2:
                self.order_table = product_table
                self.ordered.emit()
            else:
                self.statusBar.showMessage("Formularz nie może być pusty!")
                self.show_warning("Uzupełnij formularz!", "Formularz nie może być pusty!")
        except ValueError as e:
            self.show_warning("Błąd!", "Wprowadź ilość zamawianego towaru")
            print(e)

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)
        self.code.setFocus()


class OrderWindow(QtWidgets.QMainWindow, order.Ui_MainWindow):
    confirmed = QtCore.pyqtSignal()
    wiped = QtCore.pyqtSignal()
    headers = ["kod", "opis", "sztuk", "notatka"]

    def __init__(self, parent):
        self.parent = parent
        super(OrderWindow, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setupUi(self)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(4)
        self.wipe.clicked.connect(self.del_button)
        self.apply.clicked.connect(self.confirm_order)
        self.listofparameters = []

    def add_table(self, table_list):
        for i in range(1, len(table_list)):
            self.tableWidget.setItem(0, i - 1, QtWidgets.QTableWidgetItem(str(table_list[i])))
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.setHorizontalHeaderLabels(self.headers)

    def del_button(self):
        self.wiped.emit()
        self.close()

    def confirm_order(self):
        global dir_output_files_orders
        output_file_dir = f"{dir_output_files_orders}/zamowienie_{str(datetime.datetime.today()).split()[0]}.csv"
        db = Database.DataBase()
        db.create_connection()
        params = self.listofparameters
        orderer = params[0]
        code = params[1]
        info = params[2]
        val = params[3]
        note = params[4]
        correctly_added = db.add_order(orderer, code, info, val, note)
        if correctly_added:
            csv_writer(output_file_dir,[orderer, code, info, val, note])
            self.show_msg("Dodano", "Zamówienie zostało złożone")
            self.wiped.emit()
            self.close()
        else:
            self.show_error("Błąd!", "Błąd przy dodawaniu do bazy danych!\nSprawdź połączenie z internetem.\n"
                                     "Jeśli nie pomoże, skontaktuj się z PCLAND")

    def show_msg(self, title, message):
        QMessageBox.about(self, title, message)

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)


class UsersWindow(QtWidgets.QMainWindow, add_user.Ui_MainWindow):

    def __init__(self, parent=None):
        super(UsersWindow, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setupUi(self)
        self.submit.clicked.connect(self.submited)
        self.show_passwd_button.clicked.connect(self.show_users_passwd)
        self.button_remove.clicked.connect(self.delete_user)
        self.button_modify_password.clicked.connect(self.edit_password)
        self.access_confirm.clicked.connect(self.manage_access)

    def submited(self):
        password1 = self.passwd.text()
        password2 = self.con_passwd.text()
        name = self.login.text()
        if password1 != password2:
            self.show_warning("Niezgodność haseł", "Hasła się nie zgadzają")
            self.passwd.clear()
            self.con_passwd.clear()
            self.passwd.setFocus()
            return False

        db = Database.DataBase()
        db.create_connection()
        ret = 0
        if self.both.isChecked():
            user_args = (name, password1, 1, 1)
            ret = db.add_user(user_args)

        elif self.order.isChecked():
            user_args = (name, password1, 1, 0)
            ret = db.add_user(user_args)

        elif self.delivery.isChecked():
            user_args = (name, password1, 0, 1)
            ret = db.add_user(user_args)

        if ret == 1:
            self.show_warning("Dodano", f"Użytkownik {name} został dodany.")
        elif ret == -2:
            self.show_warning("Błąd", f"Użytkownik {name} istnieje.\nWybierz inną nazwę.")
        elif ret == -1:
            self.show_warning("Błąd", "Przekroczono czas połączenia, spróbuj ponownie.")
        self.refresh_users_table()

    def refresh_users_table(self, show_passwd=False):
        db = Database.DataBase()
        db.create_connection()
        self.tableWidget.setRowCount(0)  # clear data from table
        users = db.list_all_users()
        try:
            if type(users) == int:
                print("Błąd")
        except TypeError:
            self.show_warning("Błąd", "Brak użytkowników")
        counter = 0
        for user in users:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for i in range(0, 5):
                if not show_passwd and i == 2:
                    self.tableWidget.setItem(counter, i, QtWidgets.QTableWidgetItem("*****"))
                else:
                    self.tableWidget.setItem(counter, i, QtWidgets.QTableWidgetItem(str(user[i])))
            counter += 1
        self.tableWidget.resizeColumnsToContents()

    def show_users_passwd(self):
        self.refresh_users_table(True)

    def delete_user(self):
        db = Database.DataBase()
        db.create_connection()
        ID = self.remove_user_id.text()
        if db.delete_user(ID):
            self.show_warning("Usunięto", f"Użytkownik o ID {ID} został usunięty.")
        else:
            self.show_warning("Błąd!", "Nie udało się usunąć użytkownika.\nSprawdź wprowadzone ID")
        self.refresh_users_table()

    def edit_password(self):
        user_id = self.edit_ID.text()
        passwd1 = self.edit_passwd.text()
        passwd2 = self.edit_repasswd.text()
        db = Database.DataBase()
        db.create_connection()

        if passwd1 != passwd2:
            self.show_warning("Błąd", "Wprowadzone hasła się różnią")
            self.edit_passwd.clear()
            self.edit_repasswd.clear()
            self.edit_passwd.setFocus()
            return
        if db.modify_user_passwd(user_id, passwd1):
            self.show_warning("Zaktualizowano", "Hasło zostało zaktualizowane")
            self.refresh_users_table()
        else:
            self.show_warning("Błąd", "Wprowadzono błędne ID użytkownika")

    def manage_access(self):
        user_id = self.access_id.text()
        orderers = self.check_orders.isChecked()
        deliveries = self.check_delivery.isChecked()
        if orderers:
            order = 1
        else:
            order = 0
        if deliveries:
            delivery = 1
        else:
            delivery = 0
        db = Database.DataBase()
        db.create_connection()
        if db.update_user_access(user_id, order, delivery):
            self.show_warning("Zaktualizowano", "Uprawnienia użytkownika zostały zaktualizowane")
        else:
            self.show_warning("Błąd", "Podano nieistniejący numer ID")
        self.access_id.clear()
        self.refresh_users_table()

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)



class Controller:
    def __init__(self):
        self.curr_user = ""
        self.product_code = ""
        self.nr_delivery = ""
        self.orderer_list = ""
        self.added_table = []
        # initialize windows
        self.login_window = LoginWindow()
        self.window_delivery = MainWindowDelivery()
        self.ordered_table = OrderedTable(self.window_delivery)
        self.window_users = MainWindowUsers()
        self.modules = ModuleWindow()
        self.window_order = MainWindowOrder()
        self.window_order_table = OrderWindow(self.window_order)
        self.users_window = UsersWindow()
        # login
        self.login_window.logged.connect(self.modules.show)
        self.login_window.order.connect(self.open_order_window)
        self.login_window.delivery.connect(self.open_delivery_window)
        # modules
        self.modules.order.clicked.connect(self.open_order_window)
        self.modules.delivery.clicked.connect(self.open_delivery_window)
        self.modules.users.clicked.connect(self.open_users_window)
        # orders
        self.window_order.ordered.connect(self.prepare_order_table)
        self.window_order_table.wiped.connect(self.wipe_order_window)
        # delivery
        self.window_delivery.ordered.connect(self.open_delivery_table)
        self.window_delivery.exit.connect(self.save_and_exit)
        self.ordered_table.ordered.connect(self.prepare_added_delivery_table)
        self.ordered_table.gen_xls.connect(self.save_and_exit)
        # users
        # start program
        self.login_window.show()

    # orders
    def open_order_window(self):
        self.curr_user = self.login_window.input_login.text().upper()
        username = self.curr_user
        self.window_order.username.setText(username)
        self.window_order.show()

    def wipe_order_window(self):
        self.window_order.wipe.click()
        self.window_order.code.setFocus()

    def prepare_order_table(self):
        table = self.window_order.order_table
        self.window_order_table.add_table(table)
        self.window_order_table.listofparameters = table
        self.window_order_table.show()

    # delivery
    def open_delivery_window(self):
        self.window_delivery = MainWindowDelivery()
        self.curr_user = self.login_window.input_login.text()
        print(self.curr_user, self.nr_delivery)
        self.window_delivery.show()

    def open_delivery_table(self):
        self.window_delivery.delivery_nr.setEnabled(False)
        self.orderer_list = self.window_delivery.product_list
        print("lista: ", self.orderer_list)
        self.product_code = self.window_delivery.product
        self.ordered_table.add_table(self.orderer_list)
        self.ordered_table.nr_delivery = self.nr_delivery
        self.ordered_table.product_id = self.orderer_list[-1]
        self.ordered_table.show()

    def prepare_added_delivery_table(self):
        order_date = self.orderer_list[1]
        code = self.orderer_list[0]
        note = self.orderer_list[3]
        orderer = self.orderer_list[2]
        self.added_table.append([order_date, code, note, orderer])

    def save_and_exit(self):
        global dir_output_files_delivery
        self.nr_delivery = self.window_delivery.delivery
        if len(self.added_table) == 0:
            self.window_delivery.show_message("Koniec pracy.", "Brak zaktualizowanych produktów")
            self.window_delivery.close()
            self.ordered_table.close()
        if not os.path.isdir(dir_output_files_delivery):
            os.mkdir(dir_output_files_delivery)
        today_date = str(datetime.datetime.today()).split()[0]
        xlsx_namefile = f'{dir_output_files_delivery}/DOSTAWA_{self.nr_delivery}_{today_date}.xlsx'
        columns_name = ["data_zamówienia", "kod", "notatka", "zamawiający"]
        if os.path.isfile(xlsx_namefile):
            print("File exists!")
            self.ordered_table.show_warning_message("Błąd zapisu pliku .xlsx", f"Plik {xlsx_namefile} już istnieje!, "
                                                                               f"Przenieś go w inne miejsce, lub "
                                                                               f"zmień jego nazwę, aby utworzyć nowy "
                                                                               f"plik dostawy")
        else:
            workbook = xlsxwriter.Workbook(xlsx_namefile)
            worksheet = workbook.add_worksheet()
            worksheet.write_row(0, 0, columns_name)
            for i in range(0, len(self.added_table)):
                worksheet.write_row(i+1, 0, self.added_table[i])
            workbook.close()
            self.ordered_table.show_warning_message("Zapisano", f"Plik dostawy został zapisany jako: {xlsx_namefile.split('/')[1]}")
            self.window_delivery.close()
            self.ordered_table.close()

    # users
    def open_users_window(self):
        self.curr_user = self.login_window.input_login.text()
        self.users_window.frame_remove_user.hide()
        self.users_window.frame_edit_passwd.hide()
        self.users_window.frame_access.hide()
        self.users_window.refresh_users_table()
        self.users_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Controller()
    sys.exit(app.exec_())
