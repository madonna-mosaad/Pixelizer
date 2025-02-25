from PyQt5 import QtCore, QtGui, QtWidgets
from app.utils.clean_cache import remove_directories
from app.services.image_service import ImageServices
from app.design.design import Ui_MainWindow
from app.processing.EdgeDetection import EdgeDetection
from app.services.image_histogram import ImageHistogram

import cv2


class MainWindowController:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.MainWindow = QtWidgets.QMainWindow()

        self.path = None
        self.original_image = None
        self.processed_image = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.edge = EdgeDetection()

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
        self.ui.sobel_edge_detection_button.clicked.connect(self.controller_apply_sobel)
        self.ui.roberts_edge_detection_button.clicked.connect(self.controller_apply_roberts)
        self.ui.prewitt_edge_detection_button.clicked.connect(self.controller_apply_prewitt)
        self.ui.canny_edge_detection_button.clicked.connect(self.controller_apply_canny)

        self.ui.show_metrics_button.clicked.connect(lambda: ImageHistogram.show_histogram_popup(self.path))

    def controller_apply_sobel(self):
        if self.original_image is None:
            print("No image loaded. Please upload an image first.")
            return  # Prevents crashing
        self.processed_image = self.edge.apply_sobel(self.original_image)
        if self.processed_image is None:
            print("Error: Processed image is None.")
            return  # Prevents crashing
        ImageServices.clear_image(self.ui.processed_groupBox)
        ImageServices.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def controller_apply_roberts(self):
        if self.original_image is None:
            print("No image loaded. Please upload an image first.")
            return  # Prevents crashing
        self.processed_image = self.edge.apply_roberts(self.original_image)
        if self.processed_image is None:
            print("Error: Processed image is None.")
            return  # Prevents crashing
        ImageServices.clear_image(self.ui.processed_groupBox)
        ImageServices.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def controller_apply_prewitt(self):
        if self.original_image is None:
            print("No image loaded. Please upload an image first.")
            return  # Prevents crashing
        self.processed_image = self.edge.apply_prewitt(self.original_image)
        if self.processed_image is None:
            print("Error: Processed image is None.")
            return  # Prevents crashing
        ImageServices.clear_image(self.ui.processed_groupBox)
        ImageServices.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def controller_apply_canny(self):
        if self.original_image is None:
            print("No image loaded. Please upload an image first.")
            return  # Prevents crashing

        low = self.ui.edge_detection_low_threshold_spinbox.value()
        high = self.ui.edge_detection_high_threshold_spinbox.value()
        self.processed_image = self.edge.apply_canny(self.original_image, low, high)

        if self.processed_image is None:
            print("Error: Processed image is None.")
            return  # Prevents crashing
        ImageServices.clear_image(self.ui.processed_groupBox)
        ImageServices.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def drawImage(self):
        self.path = ImageServices.upload_image_file()
        self.original_image = cv2.imread(self.path)
        self.processed_image = self.original_image

        # If user cancels file selection, path could be None
        if self.path:
            ImageServices.clear_image(self.ui.original_groupBox)
            ImageServices.clear_image(self.ui.processed_groupBox)
            ImageServices.set_image_in_groupbox(self.ui.original_groupBox, self.original_image)
            ImageServices.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def closeApp(self):
        """Close the application."""
        remove_directories()
        self.app.quit()
