from PyQt5 import QtCore, QtGui, QtWidgets
from app.utils.clean_cache import remove_directories
from app.services.image_service import ImageServices
from app.design.design import Ui_MainWindow


# from app.tests.design_test import Ui_MainWindow


class MainWindowController:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        # Connect signals to slots
        self.setupConnections()

    def run(self):
        """Run the application."""
        self.MainWindow.showFullScreen()
        self.app.exec_()

    def setupConnections(self):
        """Connect buttons to their respective methods."""
        self.ui.quit_app_button.clicked.connect(self.closeApp)
        self.ui.upload_button.clicked.connect(self.drawImage)

    def drawImage(self):
        path = ImageServices.upload_image_file()

        # If user cancels file selection, path could be None
        if path:
            ImageServices.clear_image(self.ui.original_groupBox)
            ImageServices.set_image_in_groupbox(self.ui.original_groupBox, path)

    def closeApp(self):
        """Close the application."""
        remove_directories()
        self.app.quit()
