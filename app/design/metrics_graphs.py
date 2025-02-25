from PyQt5 import QtCore, QtGui, QtWidgets
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

    def setupUi(self, Dialog):
        screen = QtWidgets.QApplication.primaryScreen().size()
        width = int(screen.width() * 0.75)  # 75% of the screen width
        height = int(screen.height() * 0.9)  # 90% of the screen height

        Dialog.setObjectName("Dialog")
        Dialog.resize(width, height)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Frameless window
        Dialog.setStyleSheet("background-color: rgb(10, 10, 10);")

        # Calculate center position
        centerX = (screen.width() - width) // 2
        centerY = (screen.height() - height) // 2
        Dialog.move(centerX, centerY)  # Move window to center

        self.layout = QtWidgets.QVBoxLayout(Dialog)  # Set layout on QDialog directly
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        group_box_style = "color: white; border: 1px solid white;"

        self.histogram_groupBox, self.histogram_plot_widget = self.util.createGroupBox(
            "Histogram",
            QtCore.QSize(int(width * 0.95), int(height * 0.4)),
            group_box_style,
            isGraph=True
        )
        self.layout.addWidget(self.histogram_groupBox)

        self.distribution_groupBox, self.distribution_plot_widget = self.util.createGroupBox(
            "Distribution Curve",
            QtCore.QSize(int(width * 0.95), int(height * 0.4)),
            group_box_style,
            isGraph=True
        )
        self.layout.addWidget(self.distribution_groupBox)

        self.close_button = self.util.createButton("Close", self.button_style)
        self.close_button.clicked.connect(Dialog.accept)  # Close the dialog on button click

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.close_button)
        self.buttonLayout.addStretch(1)
        self.layout.addLayout(self.buttonLayout)

    def show_popup(self):
        """ Method to show the pop-up window as a modal dialog. """
        self.Dialog = QtWidgets.QDialog()
        self.setupUi(self.Dialog)
        self.Dialog.exec_()
