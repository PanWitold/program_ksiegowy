# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(390, 400)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.splitter_3 = QtWidgets.QSplitter(self.widget)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter = QtWidgets.QSplitter(self.splitter_3)
        self.splitter.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.splitter.setAutoFillBackground(True)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.label_2 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_3)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.username = QtWidgets.QLineEdit(self.splitter_2)
        self.username.setEnabled(False)
        self.username.setObjectName("username")
        self.code = QtWidgets.QLineEdit(self.splitter_2)
        self.code.setMaxLength(14)
        self.code.setObjectName("code")
        self.info = QtWidgets.QLineEdit(self.splitter_2)
        self.info.setMaxLength(21)
        self.info.setObjectName("info")
        self.val = QtWidgets.QLineEdit(self.splitter_2)
        self.val.setObjectName("val")
        self.note = QtWidgets.QLineEdit(self.splitter_2)
        self.note.setMaxLength(30)
        self.note.setObjectName("note")
        self.gridLayout_2.addWidget(self.splitter_3, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, -1)
        self.horizontalLayout.setSpacing(40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.order = QtWidgets.QPushButton(self.widget)
        self.order.setObjectName("order")
        self.horizontalLayout.addWidget(self.order)
        self.wipe = QtWidgets.QPushButton(self.widget)
        self.wipe.setObjectName("wipe")
        self.horizontalLayout.addWidget(self.wipe)
        self.horizontalLayout.setStretch(0, 50)
        self.horizontalLayout.setStretch(1, 50)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.code.returnPressed.connect(self.info.setFocus)
        self.info.returnPressed.connect(self.val.setFocus)
        self.val.returnPressed.connect(self.note.setFocus)
        self.wipe.clicked.connect(self.code.clear)
        self.wipe.clicked.connect(self.info.clear)
        self.wipe.clicked.connect(self.val.clear)
        self.wipe.clicked.connect(self.note.clear)
        self.note.returnPressed.connect(self.order.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.username, self.code)
        MainWindow.setTabOrder(self.code, self.info)
        MainWindow.setTabOrder(self.info, self.val)
        MainWindow.setTabOrder(self.val, self.note)
        MainWindow.setTabOrder(self.note, self.order)
        MainWindow.setTabOrder(self.order, self.wipe)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Zamówienia"))
        self.label.setText(_translate("MainWindow", "WPROWADZANIE ZAMÓWIENIA"))
        self.label_2.setText(_translate("MainWindow", "ZAMAWIAJĄCY"))
        self.label_3.setText(_translate("MainWindow", "KOD"))
        self.label_4.setText(_translate("MainWindow", "OPIS"))
        self.label_5.setText(_translate("MainWindow", "SZTUK"))
        self.label_6.setText(_translate("MainWindow", "NOTATKA"))
        self.val.setInputMask(_translate("MainWindow", "00"))
        self.order.setText(_translate("MainWindow", "ZATWIERDŹ"))
        self.wipe.setText(_translate("MainWindow", "WYCZYŚĆ"))
