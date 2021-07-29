import database_mysql as Database
import os
import datetime
import xlsxwriter

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from templates.dodawanie_kont import add_user
from templates.dostawy import main_window, ordered_table
from templates.zamowienia import main, order
from templates import login, moduly

dir_output_files = "dostawa"


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

        if db_return == [1,1]:
            #todo zmienić rodzaj weryfikacji
            print("Authorization passed")
            self.logged.emit()
            self.close()
        elif db_return == [0,1]:
            self.delivery.emit()
            self.close()
        elif db_return == [1,0]:
            self.order.emit()
            self.close()
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
        if self.product == "":
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
            print(table_list[i])
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


class Main_window(QtWidgets.QMainWindow, main.Ui_MainWindow):
    order_table = []
    ordered = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Main_window, self).__init__(parent)
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


class Controller:
    def __init__(self):
        self.product_code = ""
        self.curr_user = ""
        self.nr_delivery = ""
        self.orderer_list = ""
        self.added_table = []

        self.login_window = LoginWindow()
        self.window_delivery = MainWindowDelivery()
        self.ordered_table = OrderedTable(self.window_delivery)
        self.window_users = MainWindowUsers()
        self.modules = ModuleWindow()

        self.login_window.logged.connect(self.modules.show)
        self.login_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Controller()
    sys.exit(app.exec_())
