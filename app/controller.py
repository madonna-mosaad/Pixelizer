from PyQt5 import QtWidgets
from app.utils.clean_cache import remove_directories
from app.services.image_service import ImageServices
from app.design.main_layout import Ui_MainWindow
from app.processing.EdgeDetection import EdgeDetection
from app.processing.histogram import ImageHistogram

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

        self.srv = ImageServices()

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
        self.ui.save_image_button.clicked.connect(lambda: self.srv.save_image(self.processed_image))

        self.ui.reset_image_button.clicked.connect(self.reset_images)
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
        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def controller_apply_roberts(self):
        if self.original_image is None:
            print("No image loaded. Please upload an image first.")
            return  # Prevents crashing
        self.processed_image = self.edge.apply_roberts(self.original_image)
        if self.processed_image is None:
            print("Error: Processed image is None.")
            return  # Prevents crashing
        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def controller_apply_prewitt(self):
        if self.original_image is None:
            print("No image loaded. Please upload an image first.")
            return  # Prevents crashing
        self.processed_image = self.edge.apply_prewitt(self.original_image)
        if self.processed_image is None:
            print("Error: Processed image is None.")
            return  # Prevents crashing
        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

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
        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def drawImage(self):
        self.path = self.srv.upload_image_file()
        self.original_image = cv2.imread(self.path)
        self.processed_image = self.original_image

        # If user cancels file selection, path could be None
        if self.path:
            self.srv.clear_image(self.ui.original_groupBox)
            self.srv.clear_image(self.ui.processed_groupBox)
            self.srv.set_image_in_groupbox(self.ui.original_groupBox, self.original_image)
            self.srv.set_image_in_groupbox(self.ui.processed_groupBox, self.processed_image)

    def reset_images(self):
        self.srv.clear_image(self.ui.processed_groupBox)
        self.srv.clear_image(self.ui.original_groupBox)

    def closeApp(self):
        """Close the application."""
        remove_directories()
        self.app.quit()
