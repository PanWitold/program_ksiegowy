import Database
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from templates.zamowienia import main, login, order


class Login_window(QtWidgets.QMainWindow, login.Ui_LOGIN):
    logged = QtCore.pyqtSignal()
    curr_user = "GREG"

    def __init__(self, parent=None):
        super(Login_window, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.verify_user)
        self.input_login.textChanged.connect(self.statusbar.clearMessage)
        self.input_passwd.textChanged.connect(self.statusbar.clearMessage)

    def verify_user(self):
        user_login = self.input_login.text()
        user_password = str(self.input_passwd.text())
        db = Database.DataBase()
        db.create_connection()
        user_login = "admin"; user_password = "qwerty"   # TODO always logged as admin - remove it later
        login_auth = (user_login, user_password)

        if db.verify_user(login_auth, type="order"):
            print("Authorization passed")
            self.curr_user = user_login
            self.logged.emit()
            self.close()
        else:
            self.statusbar.showMessage("Błędny login/hasło")
            self.showDialog()

    def showDialog(self):
        QMessageBox.critical(self, "Błąd!", "Błędny login/hasło!")


class Main_window(QtWidgets.QMainWindow, main.Ui_MainWindow):
    order_table = []
    ordered = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Main_window, self).__init__(parent)
        self.setupUi(self)
        #self.username.setText(curr_user)
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


class OrderWindow(QtWidgets.QMainWindow, order.Ui_MainWindow):
    confirmed = QtCore.pyqtSignal()
    wiped = QtCore.pyqtSignal()

    headers = ["kod", "opis", "sztuk", "notatka"]

    def __init__(self, parent):
        self.parent = parent
        super(OrderWindow, self).__init__(parent)
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
        self.login = Login_window()
        self.main_window = Main_window()
        self.order_window = OrderWindow(self.main_window)

        self.login.logged.connect(self.get_username_from_login)
        self.main_window.ordered.connect(self.prepare_order_table)
        self.login.show()
        #self.order_window.show()
        #self.get_username_from_login()

    def get_username_from_login(self):
        username = self.login.curr_user
        self.main_window.username.setText(username)
        self.main_window.show()

    def prepare_order_table(self):
        table = self.main_window.order_table
        self.order_window.add_table(table)
        self.order_window.listofparameters = table
        self.order_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Controller()
    sys.exit(app.exec_())
