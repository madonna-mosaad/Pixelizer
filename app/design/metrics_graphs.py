from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(760, 780)
        MainWindow.setStyleSheet("background-color:#040d12;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.upload_button = QtWidgets.QPushButton(self.centralwidget)
        self.upload_button.setGeometry(QtCore.QRect(200, 700, 281, 49))
        self.upload_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.upload_button.setStyleSheet("QPushButton {\n"
                                         "                                            background-color: rgb(30, 30, 30);\n"
                                         "                                            color: white;\n"
                                         "                                            border: none;\n"
                                         "                                            padding: 10px 20px;\n"
                                         "                                            text-align: center;\n"
                                         "                                            text-decoration: none;\n"
                                         "                                            font-size: 16px;\n"
                                         "                                            margin: 4px 2px;\n"
                                         "                                            border-radius: 8px;\n"
                                         "                                            border:1px solid white;\n"
                                         "                                            }\n"
                                         "                                            QPushButton:hover {\n"
                                         "                                            background-color: rgb(40,40,40);\n"
                                         "                                            }\n"
                                         "                                        ")
        self.upload_button.setObjectName("upload_button")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 741, 691))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox_2.setStyleSheet("color:white;\n"
                                      "                                    border:1px solid white\n"
                                      "                                ")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setStyleSheet("color:white;\n"
                                    "                                    border:1px solid white\n"
                                    "                                ")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.upload_button.setText(_translate("MainWindow", "Back"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Histogram"))
        self.groupBox.setTitle(_translate("MainWindow", "Distribution Curve"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    sys.exit(app.exec_())
