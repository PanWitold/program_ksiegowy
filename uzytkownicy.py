import database_mysql as Database
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from templates.dodawanie_kont import login, add_user


class Login_window(QtWidgets.QMainWindow, login.Ui_LOGIN):
    logged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Login_window, self).__init__(parent)
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

        if db.verify_user(login_auth, "order") and db.verify_user(login_auth, "delivery"):
            print("Authorization passed")
            self.logged.emit()
            self.close()
        else:
            self.statusbar.showMessage("Błędny login/hasło")
            self.showDialog("Błąd!", "Błędny login/hasło!")

    def showDialog(self, title, msg):
        QMessageBox.critical(self, title, msg)


class Main_window(QtWidgets.QMainWindow, add_user.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Main_window, self).__init__(parent)
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


class Controller:
    def __init__(self):
        self.login_window = Login_window()
        self.main_window = Main_window()
        self.login_window.logged.connect(self.main_window.show)
        self.login_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Controller()
    sys.exit(app.exec_())
