from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from app.design.tools.gui_utilities import GUIUtilities


class Ui_PopWindow:
    def __init__(self):
        self.util = GUIUtilities()
        self.button_style = """
            QPushButton {
                background-color: rgb(30, 30, 30);
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 8px;
                border: 1px solid white;
            }
            QPushButton:hover {
                background-color: rgb(40, 40, 40);
            }
        """

    def setupUi(self, MainWindow):
        screen = QtWidgets.QApplication.primaryScreen().size()
        width = int(screen.width() * 0.75)  # 75% of the screen width
        height = int(screen.height() * 0.9)  # 90% of the screen height

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(width, height)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Frameless window
        MainWindow.setStyleSheet("background-color: #040d12;")

        # Calculate center position
        centerX = (screen.width() - width) // 2 + 20
        centerY = (screen.height() - height) // 2 - 20
        MainWindow.move(centerX, centerY)  # Move window to center

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(20)

        group_box_style = "color: white; border: 1px solid white;"

        self.histogram_groupBox, self.histogram_plot_widget = self.util.createGroupBox(
            "Histogram",
            QtCore.QSize(int(width * 0.95), int(height * 0.4)),
            group_box_style,
            isGraph=True
        )
        self.mainLayout.addWidget(self.histogram_groupBox)

        self.distribution_groupBox, self.distribution_plot_widget = self.util.createGroupBox(
            "Distribution Curve",
            QtCore.QSize(int(width * 0.95), int(height * 0.4)),
            group_box_style,
            isGraph=True
        )
        self.mainLayout.addWidget(self.distribution_groupBox)

        self.upload_button = self.util.createButton("Back", self.button_style)
        self.upload_button.clicked.connect(MainWindow.close)  # Connect the button to close the window

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.upload_button)
        self.buttonLayout.addStretch(1)
        self.mainLayout.addLayout(self.buttonLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Metrics Popup"))
        self.upload_button.setText(_translate("MainWindow", "Back"))
        self.histogram_groupBox.setTitle(_translate("MainWindow", "Histogram"))
        self.distribution_groupBox.setTitle(_translate("MainWindow", "Distribution Curve"))

    def show_popup(self):
        """ Method to show the pop-up window. """
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.MainWindow.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    ui = Ui_PopWindow()
    ui.show_popup()
