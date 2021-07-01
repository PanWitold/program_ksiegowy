import Database
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from templates.dostawy import login, main_window, ordered_table


class LoginWindow(QtWidgets.QMainWindow, login.Ui_MainWindow):
    logged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.login.textChanged.connect(self.statusbar.clearMessage)
        self.password.textChanged.connect(self.statusbar.clearMessage)
        self.loginButton.clicked.connect(self.log_user)

    def log_user(self):
        user = self.login.text()
        password = self.password.text()
        nr_delivery = self.nrOfDelivery.text()
        if user == "" or password == "":
            print("Input name/password")
            self.show_message("Błąd.", "Wpisz login/hasło")
            self.statusbar.showMessage("Input name/password")
        elif nr_delivery == "":
            self.show_message("Wprowadź numer dostawy", "Numer dostawy nie może być pusty")
        else:
            #TODO weryfikowanie użytkownika, logowanie
            logged = True
            if logged:
                self.logged.emit()
                self.close()

        print(user, password, nr_delivery)

    def show_message(self, title, msg):
        QMessageBox.warning(self, title, msg)


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    ordered = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.order_product)

    def order_product(self):
        self.ordered.emit()


class OrderedTable(QtWidgets.QMainWindow, ordered_table.Ui_MainWindow):

    def __init__(self, parent=None):
        super(OrderedTable, self).__init__(parent)
        self.setupUi(self)


class Controller:
    def __init__(self):
        self.login = LoginWindow()
        self.main_window = MainWindow()
        self.ordered_table = OrderedTable()

        self.login.logged.connect(self.main_window.show)
        self.main_window.ordered.connect(self.ordered_table.show)

        self.login.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Controller()
    sys.exit(app.exec_())
