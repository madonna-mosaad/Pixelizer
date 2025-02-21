from PyQt5 import QtWidgets
from app.design.design import Ui_MainWindow
from app.utils.clean_cache import remove_directories


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

    def closeApp(self):
        """Close the application."""
        remove_directories()
        self.app.quit()
