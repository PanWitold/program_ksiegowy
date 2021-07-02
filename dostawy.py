import Database
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from templates.dostawy import login, main_window, ordered_table


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
            user_login = "admin1"; user_password = "qwerty"  # TODO always logged as admin - remove it later
            login_auth = (user_login, user_password)

            if db.verify_user(login_auth, type="delivery"):
                print("Authorization passed")
                self.curr_user = user_login
                self.logged.emit()
                self.close()
            else:
                self.statusbar.showMessage("Błędny login/hasło")
                self.show_message("Zły login/hasło", "Niepoprawne dane logowania")

        print(self.curr_user, self.nr_delivery)

    def show_message(self, title, msg):
        QMessageBox.warning(self, title, msg)


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    ordered = QtCore.pyqtSignal()
    product = ""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.order_product)

    def order_product(self):
        self.product = self.product_code.text()
        if self.product == "":
            self.show_message("Brak numeru", "Wprowadź kod produktu!")
        else:
            #TODO sprawdzenie czy taki numer produktu nieprzypisany do dostawy istnieje w bazie
            #jeżeli tak: \/
            # jeżeli nie to komunikat o braku zapotrzebowania na produkt o danym id
            self.ordered.emit()

    def show_message(self, title, msg):
        QMessageBox.warning(self, title, msg)


class OrderedTable(QtWidgets.QMainWindow, ordered_table.Ui_MainWindow):

    def __init__(self, parent):
        super(OrderedTable, self).__init__(parent)
        self.setupUi(self)


class Controller:
    def __init__(self):
        self.product_code = ""
        self.curr_user = ""
        self.nr_delivery = ""
        self.login = LoginWindow()
        self.main_window = MainWindow()
        self.ordered_table = OrderedTable(self.main_window)

        self.login.logged.connect(self.open_main_window)
        self.main_window.ordered.connect(self.open_order_table)

        self.login.show()

    def open_main_window(self):
        self.nr_delivery = self.login.nr_delivery
        self.curr_user = self.login.curr_user
        print(self.curr_user, self.nr_delivery)
        self.main_window.show()

    def open_order_table(self):
        self.product_code = self.main_window.product
        print(self.product_code)
        self.ordered_table.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Controller()
    sys.exit(app.exec_())
