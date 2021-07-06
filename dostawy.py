import database_mysql as Database
import os
import datetime
import xlsxwriter

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from templates.dostawy import login, main_window, ordered_table

dir_output_files = "dostawa"


class LoginWindow(QtWidgets.QMainWindow, login.Ui_MainWindow):
    logged = QtCore.pyqtSignal()
    nr_delivery = ""
    curr_user = ""

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.login.textChanged.connect(self.statusbar.clearMessage)
        self.password.textChanged.connect(self.statusbar.clearMessage)
        self.loginButton.clicked.connect(self.log_user)

    def log_user(self):
        password = self.password.text()
        self.nr_delivery = self.nrOfDelivery.text()
        self.curr_user = self.login.text()
        db = Database.DataBase()
        db.create_connection()
        if self.curr_user == "" or password == "":
            print("Input name/password")
            self.show_message("Błąd.", "Wpisz login/hasło")
            self.statusbar.showMessage("Input name/password")
        elif self.nr_delivery == "":
            self.show_message("Wprowadź numer dostawy", "Numer dostawy nie może być pusty")
        else:
            user_login = self.login.text()
            user_password = self.password.text()
            db = Database.DataBase()
            db.create_connection()
            #user_login = "admin1"; user_password = "qwerty"  # always logged as admin - remove it later
            login_auth = (user_login, user_password)

            if db.verify_user(login_auth, "delivery"):
                print("Authorization passed")
                self.curr_user = user_login
                self.logged.emit()
                self.close()
            else:
                self.statusbar.showMessage("Błędny login/hasło")
                self.show_message("Zły login/hasło", "Niepoprawne dane logowania")
                self.login.setFocus()

        print(self.curr_user, self.nr_delivery)

    def show_message(self, title, msg):
        QMessageBox.warning(self, title, msg)


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    ordered = QtCore.pyqtSignal()
    exit = QtCore.pyqtSignal()
    product = ""
    product_list = []

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
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


class Controller:
    def __init__(self):
        self.product_code = ""
        self.curr_user = ""
        self.nr_delivery = ""
        self.orderer_list = ""
        self.added_table = []

        self.login = LoginWindow()
        self.main_window = MainWindow()
        self.ordered_table = OrderedTable(self.main_window)

        self.login.logged.connect(self.open_main_window)
        self.main_window.ordered.connect(self.open_order_table)
        self.main_window.exit.connect(self.save_and_exit)
        self.ordered_table.ordered.connect(self.prepare_added_table)
        self.ordered_table.gen_xls.connect(self.save_and_exit)
        self.login.show()

    def open_main_window(self):
        self.nr_delivery = self.login.nr_delivery
        self.curr_user = self.login.curr_user
        print(self.curr_user, self.nr_delivery)
        self.main_window.show()

    def open_order_table(self):
        self.orderer_list = self.main_window.product_list
        print("lista: ", self.orderer_list)
        self.product_code = self.main_window.product
        self.ordered_table.add_table(self.orderer_list)
        self.ordered_table.nr_delivery = self.nr_delivery
        self.ordered_table.product_id = self.orderer_list[-1]
        self.ordered_table.show()

    def prepare_added_table(self):
        order_date = self.orderer_list[1]
        code = self.orderer_list[0]
        note = self.orderer_list[3]
        orderer = self.orderer_list[2]
        self.added_table.append([order_date, code, note, orderer])

    def save_and_exit(self):
        global dir_output_files
        if len(self.added_table) == 0:
            self.main_window.show_message("Koniec pracy.", "Brak zaktualizowanych produktów")
            self.main_window.close()
            self.ordered_table.close()
        today_date = str(datetime.datetime.today()).split()[0]
        xlsx_namefile = f'{dir_output_files}\DOSTAWA_{self.nr_delivery}_{today_date}.xlsx'
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
            self.ordered_table.show_warning_message("Zapisano", f"Plik dostawy został zapisany jako: {xlsx_namefile}")
            self.main_window.close()
            self.ordered_table.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Controller()
    sys.exit(app.exec_())
