import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import login, main



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = main.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowModality(False)
    MainWindow.show()

    LoginWindow = QtWidgets.QMainWindow()
    ui = login.Ui_LOGIN()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    MainWindow.setEnabled(False)

#   MainWindow.setEnabled(False)
    sys.exit(app.exec_())
