from PyQt5 import QtCore, QtGui, QtWidgets
from app.design.tools.gui_utilities import GUIUtilities
from app.design.metrics_graphs import Ui_PopWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.screen_size = QtWidgets.QApplication.primaryScreen().size()
        MainWindow.resize(self.screen_size.width(), self.screen_size.height())

        # 1) Define style variables
        self.setupStyles()
        self.util = GUIUtilities()
        self.popup = Ui_PopWindow()

        # 2) Apply main window style
        MainWindow.setStyleSheet(self.main_window_style)

        # 3) Central widget & main layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_vertical_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.main_vertical_layout.setSpacing(0)

        # 4) Create Title (icon + label) and Navbar (upload, reset, save, quit)
        self.setupTitleArea()
        self.setupNavbar()
        self.combineTitleAndNavbar()

        # Add the top bar (title+navbar) to the main vertical layout
        self.main_vertical_layout.addLayout(self.title_nav_layout)

        # 5) Create the main content: left sidebar + two group boxes on the right
        self.setupMainContent()
        self.main_vertical_layout.addLayout(self.main_content_layout)

        # 6) Finalize the main window
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu bar & status bar (if needed)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # 7) Set window title, etc.
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ----------------------------------------------------------------------
    # Styles
    # ----------------------------------------------------------------------
    def setupStyles(self):
        """Holds all style sheets in one place for easier modification."""
        self.main_window_style = "background-color: #040d12;"
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
        self.quit_button_style = """
            QPushButton {
                color: rgb(255, 255, 255);
                border: 3px solid rgb(255, 255, 255);
            }
            QPushButton:hover {
                border-color: rgb(253, 94, 80);
                color: rgb(253, 94, 80);
            }
        """
        self.groupbox_style = """
            color: white;
            border: 1px solid white;
        """
        self.slider_style = """
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 2px;
                background: #dddddd;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: rgb(11, 62, 159);
                width: 16px;
                margin: -10px 0;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: rgb(4, 29, 127);
                border: 1px solid rgb(4, 29, 127);
                height: 1px;
                border-radius: 2px;
            }
        """

    # ----------------------------------------------------------------------
    # Title + Navbar
    # ----------------------------------------------------------------------
    def setupTitleArea(self):
        """Creates the title icon & label in a horizontal layout."""
        self.title_icon = QtWidgets.QLabel()
        self.title_icon.setMaximumSize(QtCore.QSize(80, 80))
        self.title_icon.setPixmap(QtGui.QPixmap("static/icons/icon.png"))
        self.title_icon.setScaledContents(True)
        self.title_icon.setObjectName("title_icon")

        self.title_label = self.util.createLabel(
            text="Pixelizing",
            style="color:white; padding:10px; padding-left:0;",
            isHead=True
        )
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(True)
        self.title_label.setFont(font)

        # Horizontal layout for icon + label
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.addWidget(self.title_icon)
        self.title_layout.addWidget(self.title_label)

    def setupNavbar(self):
        """Creates the Upload, Reset, Save, and Quit buttons."""
        self.upload_button = self.util.createButton("Upload", self.button_style)
        self.reset_image_button = self.util.createButton("Reset", self.button_style)
        self.save_image_button = self.util.createButton("Save", self.button_style)

        self.quit_app_button = self.util.createButton("X", self.quit_button_style)
        self.util.adjust_quit_button(self.quit_app_button)

        self.navbar_layout = QtWidgets.QHBoxLayout()
        self.navbar_layout.setSpacing(25)
        self.navbar_layout.addWidget(self.upload_button)
        self.navbar_layout.addWidget(self.reset_image_button)
        self.navbar_layout.addWidget(self.save_image_button)
        self.navbar_layout.addWidget(self.quit_app_button)

    def combineTitleAndNavbar(self):
        """Combines the title & navbar in one horizontal layout."""
        self.title_nav_layout = QtWidgets.QHBoxLayout()
        self.title_nav_layout.addLayout(self.title_layout)
        self.title_nav_layout.addStretch(1)
        self.title_nav_layout.addLayout(self.navbar_layout)

    # ----------------------------------------------------------------------
    # Main Content: Sidebar + GroupBoxes
    # ----------------------------------------------------------------------
    def setupMainContent(self):
        """
        Creates a horizontal layout that includes:
         - A stacked sidebar (main buttons vs. noise controls)
         - Two group boxes (Original & Processed) side-by-side
        """
        self.main_content_layout = QtWidgets.QHBoxLayout()
        self.main_content_layout.setSpacing(10)

        # 1) Sidebar (QStackedWidget)
        self.setupSidebarStack()
        self.main_content_layout.addWidget(self.sidebar_stacked)

        # 2) Group Boxes
        self.setupImageGroupBoxes()
        images_layout = QtWidgets.QHBoxLayout()
        images_layout.setSpacing(10)
        images_layout.addWidget(self.original_groupBox)
        images_layout.addWidget(self.processed_groupBox)

        self.main_content_layout.addLayout(images_layout)

    # ----------------------------------------------------------------------
    # Sidebar with QStackedWidget
    # ----------------------------------------------------------------------
    def setupSidebarStack(self):
        """
        Creates a QStackedWidget with two pages:
          Page 0 = main sidebar buttons
          Page 1 = noise controls + "Back" button
        """
        # The stacked widget
        self.sidebar_stacked = QtWidgets.QStackedWidget()
        self.sidebar_stacked.setMinimumWidth(250)  # Adjust as needed
        # You could also set a minimum height if desired

        # PAGE 0: Main Buttons
        self.page_main_buttons = QtWidgets.QWidget()
        self.page_main_buttons_layout = QtWidgets.QVBoxLayout(self.page_main_buttons)
        self.page_main_buttons_layout.setSpacing(25)

        self.setupMainButtons()  # Creates the main buttons
        # Add them to the page_main_buttons_layout
        for btn in self.MAIN_BUTTONS:
            self.page_main_buttons_layout.addWidget(btn)

        self.sidebar_stacked.addWidget(self.page_main_buttons)

        # PAGE 1: Noise Controls
        self.page_noise_controls = QtWidgets.QWidget()
        self.page_noise_layout = QtWidgets.QVBoxLayout(self.page_noise_controls)
        self.page_noise_layout.setSpacing(10)

        # Add noise widgets to page_noise_layout
        self.setupNoiseWidgets()
        self.sidebar_stacked.addWidget(self.page_noise_controls)

        # PAGE 2: Filter Controls
        self.page_filter_controls = QtWidgets.QWidget()
        self.page_filter_layout = QtWidgets.QVBoxLayout(self.page_filter_controls)
        self.page_filter_layout.setSpacing(10)

        # Add noise widgets to page_noise_layout
        self.setupFilterWidgets()
        self.sidebar_stacked.addWidget(self.page_filter_controls)

        # PAGE 3: Edge Detection Controls
        self.page_edge_detection_controls = QtWidgets.QWidget()
        self.page_edge_detection_layout = QtWidgets.QVBoxLayout(self.page_edge_detection_controls)
        self.page_edge_detection_layout.setSpacing(10)

        # Add noise widgets to page_noise_layout
        self.setupEdgeDetectionWidgets()
        self.sidebar_stacked.addWidget(self.page_edge_detection_controls)

        # PAGE 4: Refine Image Controls
        self.page_refine_image_controls = QtWidgets.QWidget()
        self.page_refine_image_layout = QtWidgets.QVBoxLayout(self.page_refine_image_controls)
        self.page_refine_image_layout.setSpacing(10)

        # Add noise widgets to page_noise_layout
        self.setupRefineImageWidgets()
        self.sidebar_stacked.addWidget(self.page_refine_image_controls)

        # PAGE 5: Fourier Filter Controls
        self.page_fourier_filter_controls = QtWidgets.QWidget()
        self.page_fourier_filter_layout = QtWidgets.QVBoxLayout(self.page_fourier_filter_controls)
        self.page_fourier_filter_layout.setSpacing(10)

        # Add noise widgets to page_noise_layout
        self.setupFourierFilterWidgets()
        self.sidebar_stacked.addWidget(self.page_fourier_filter_controls)

        # By default, show page 0
        self.sidebar_stacked.setCurrentIndex(0)

    def setupMainButtons(self):
        """
        Creates the main sidebar buttons list (Noise, Filters, etc.),
        plus sets up references so we can hide them if we want.
        """
        self.show_noise_options_button = self.util.createButton(
            "Noise", self.button_style, self.show_noise_controls
        )
        self.show_filter_options_button = self.util.createButton("Filters", self.button_style, self.show_filter_controls)
        self.show_edge_detecting_options_button = self.util.createButton("Edge Detector", self.button_style, self.show_edge_detection_controls)
        self.show_metrics_button = self.util.createButton("View Metrics", self.button_style)
        self.show_refine_options_button = self.util.createButton("Refine Image", self.button_style, self.show_refine_image_controls)
        self.show_threshold_options_button = self.util.createButton("Thresholding", self.button_style)
        self.grayscaling_button = self.util.createButton("Gray Scaling", self.button_style)
        self.show_fourier_filter_options_button = self.util.createButton("Fourier Filters", self.button_style, self.show_fourier_filter_controls)
        self.upload_hybrid_image_button = self.util.createButton("Hybrid Image", self.button_style)

        # We'll store these main buttons in a list if you need to show/hide them
        self.MAIN_BUTTONS = [
            self.show_noise_options_button,
            self.show_filter_options_button,
            self.show_edge_detecting_options_button,
            self.show_metrics_button,
            self.show_refine_options_button,
            self.show_threshold_options_button,
            self.grayscaling_button,
            self.show_fourier_filter_options_button,
            self.upload_hybrid_image_button
        ]
        self.kernal_sizes_array = ["3×3", "4×4", "5×5"]

    def setupNoiseWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """

        # Back button used on the Noise page
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_noise_layout.addWidget(back_button)

        # Uniform Noise
        uniform_title = self.util.createLabel("Uniform Noise", "Color:white;", isVisible=True, isHead=True)
        self.page_noise_layout.addWidget(uniform_title)

        uniform_label = self.util.createLabel("Noise Amount", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(uniform_label)

        (self.uniform_noise_slider,
         uniform_slider_label,
         uniform_slider_layout) = self.util.createSlider(unit="%", style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(uniform_slider_layout)
        self.uniform_noise_button = self.util.createButton("Apply", self.button_style)
        self.page_noise_layout.addWidget(self.uniform_noise_button)

        # Gaussian Noise
        gaussian_title = self.util.createLabel("Gaussian Noise", "Color:white;", isVisible=True, isHead=True)
        self.page_noise_layout.addWidget(gaussian_title)

        mean_label = self.util.createLabel("Mean", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(mean_label)

        (self.mean_gaussian_noise_slider,
         mean_slider_label,
         mean_slider_layout) = self.util.createSlider(min_value=-5, max_value=5, initial_value=0, style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(mean_slider_layout)

        # This second label was "Mean" in your original code
        stddev_label = self.util.createLabel("Standard Deviation", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(stddev_label)

        (self.stddev_gaussian_noise_slider,
         stddev_val_label,
         stddev_layout) = self.util.createSlider(min_value=0, max_value=10, initial_value=5, style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(stddev_layout)

        self.gaussian_noise_button = self.util.createButton("Apply", self.button_style)
        self.page_noise_layout.addWidget(self.gaussian_noise_button)

        # Salt & Pepper Noise
        salt_pepper_noise_title = self.util.createLabel("Salt & Pepper Noise", "Color:white;", isVisible=True, isHead=True)
        self.page_noise_layout.addWidget(salt_pepper_noise_title)

        salt_pepper_noise_label = self.util.createLabel("Noise Amount", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(salt_pepper_noise_label)

        (self.salt_pepper_noise_slider,
         uniform_slider_label,
         uniform_slider_layout) = self.util.createSlider(unit="%", style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(uniform_slider_layout)
        self.salt_pepper_noise_button = self.util.createButton("Apply", self.button_style)
        self.page_noise_layout.addWidget(self.salt_pepper_noise_button)

    def setupFilterWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """
        # Back button used on the Filter page
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_filter_layout.addWidget(back_button)

        kernal_size_label = self.util.createLabel("Kernal Size", isHead=True)
        self.page_filter_layout.addWidget(kernal_size_label)
        self.filter_kernal_size_button = self.util.createButton(self.kernal_sizes_array[0], self.button_style, lambda: self.toggle_kernal_size(self.filter_kernal_size_button))
        self.page_filter_layout.addWidget(self.filter_kernal_size_button)

        average_filter_title = self.util.createLabel("Average Filter", "color:white;", isVisible=True, isHead=True)
        self.page_filter_layout.addWidget(average_filter_title)
        self.average_filter_button = self.util.createButton("Apply", self.button_style)
        self.page_filter_layout.addWidget(self.average_filter_button)

        gaussian_filter_title = self.util.createLabel("Gaussian Filter", "color:white;", isVisible=True, isHead=True)
        self.page_filter_layout.addWidget(gaussian_filter_title)
        gaussian_filter_sigma_label = self.util.createLabel("Sigma - σ", "Color:white;", isVisible=True)
        self.page_filter_layout.addWidget(gaussian_filter_sigma_label)
        (self.gaussian_filter_sigma_spinbox,
         uniform_slider_label,
         uniform_slider_layout) = self.util.createSpinBox(0, 10, 1)
        self.page_filter_layout.addLayout(uniform_slider_layout)
        self.gaussian_filter_apply_button = self.util.createButton("Apply", self.button_style)
        self.page_filter_layout.addWidget(self.gaussian_filter_apply_button)

        median_filter_title = self.util.createLabel("Median Filter", "color:white;", isVisible=True, isHead=True)
        self.page_filter_layout.addWidget(median_filter_title)
        self.median_filter_button = self.util.createButton("Apply", self.button_style)
        self.page_filter_layout.addWidget(self.median_filter_button)

    def setupEdgeDetectionWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_edge_detection_layout.addWidget(back_button)

        # =========================================================================================================
        sobel_label = self.util.createLabel("Sobel Edge", isHead=True)
        self.page_edge_detection_layout.addWidget(sobel_label)
        self.sobel_edge_detection_button = self.util.createButton("Apply", self.button_style)
        self.page_edge_detection_layout.addWidget(self.sobel_edge_detection_button)

        # =========================================================================================================
        roberts_label = self.util.createLabel("Roberts Edge", isHead=True)
        self.page_edge_detection_layout.addWidget(roberts_label)
        self.roberts_edge_detection_button = self.util.createButton("Apply", self.button_style)
        self.page_edge_detection_layout.addWidget(self.roberts_edge_detection_button)

        # =========================================================================================================
        canny_label = self.util.createLabel("Canny Edge", isHead=True)
        self.page_edge_detection_layout.addWidget(canny_label)

        high_threshold_label = self.util.createLabel("High Threshold")
        self.page_edge_detection_layout.addWidget(high_threshold_label)

        (self.edge_detection_high_threshold_spinbox,
         edge_detection_high_threshold_label,
         edge_detection_high_threshold_layout) = self.util.createSpinBox(0, 100, 50)
        self.page_edge_detection_layout.addLayout(edge_detection_high_threshold_layout)
        self.edge_detection_high_threshold_spinbox.valueChanged.connect(self.update_low_threshold)

        low_threshold_label = self.util.createLabel("Low Threshold")
        self.page_edge_detection_layout.addWidget(low_threshold_label)

        (self.edge_detection_low_threshold_spinbox,
         edge_detection_low_threshold_label,
         edge_detection_low_threshold_layout) = self.util.createSpinBox(0, 100, 50)

        self.page_edge_detection_layout.addLayout(edge_detection_low_threshold_layout)
        self.edge_detection_low_threshold_spinbox.valueChanged.connect(self.update_high_threshold)

        self.canny_edge_detection_button = self.util.createButton("Apply", self.button_style)
        self.page_edge_detection_layout.addWidget(self.canny_edge_detection_button)

        # =========================================================================================================
        prewitt_label = self.util.createLabel("Prewitt Edge", isHead=True)
        self.page_edge_detection_layout.addWidget(prewitt_label)
        self.prewitt_edge_detection_button = self.util.createButton("Apply", self.button_style)
        self.page_edge_detection_layout.addWidget(self.prewitt_edge_detection_button)

    def setupRefineImageWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_refine_image_layout.addWidget(back_button)

        # =========================================================================================================
        normalize_label = self.util.createLabel("Normalize", isHead=True)
        self.page_refine_image_layout.addWidget(normalize_label)
        self.normalize_image_button = self.util.createButton("Apply", self.button_style)
        self.page_refine_image_layout.addWidget(self.normalize_image_button)

        # =========================================================================================================
        equalize_label = self.util.createLabel("Equalize", isHead=True)
        self.page_refine_image_layout.addWidget(equalize_label)
        self.equalize_image_button = self.util.createButton("Apply", self.button_style)
        self.page_refine_image_layout.addWidget(self.equalize_image_button)

        # =========================================================================================================
        label01 = self.util.createLabel("", isHead=True)
        self.page_refine_image_layout.addWidget(label01)
        label02 = self.util.createLabel("", isHead=True)
        self.page_refine_image_layout.addWidget(label02)

    def setupFourierFilterWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """
        back_button = self.util.createButton("Back", self.button_style, self.show_main_buttons)
        self.page_fourier_filter_layout.addWidget(back_button)

        # =========================================================================================================
        pass_filter_label = self.util.createLabel("Current Pass Filter", isHead=True)
        self.page_fourier_filter_layout.addWidget(pass_filter_label)
        self.pass_filter_button = self.util.createButton("High Pass Filter", self.button_style, self.toggle_pass_filter)
        self.page_fourier_filter_layout.addWidget(self.pass_filter_button)

        # =========================================================================================================
        raduis_control_title = self.util.createLabel("Raduis Control", isHead=True)
        self.page_fourier_filter_layout.addWidget(raduis_control_title)
        (self.raduis_control_slider,
         raduis_control_label,
         raduis_control_layout) = self.util.createSlider(0, 100, 50, "%", self.slider_style, )
        self.page_fourier_filter_layout.addLayout(raduis_control_layout)

        label01 = self.util.createLabel("", isHead=True)
        self.page_fourier_filter_layout.addWidget(label01)
        label02 = self.util.createLabel("", isHead=True)
        self.page_fourier_filter_layout.addWidget(label02)
        label03 = self.util.createLabel("", isHead=True)
        self.page_fourier_filter_layout.addWidget(label03)

    def toggle_kernal_size(self, kernal_button):
        """
        Cycles through predefined kernel sizes and updates the button text to reflect the current selection.
        """
        # Get the current text of the button
        current_text = kernal_button.text()

        # Find the index of the current text in the kernel sizes array
        current_index = self.kernal_sizes_array.index(current_text)

        # Compute the next index; wrap around to the beginning if necessary
        next_index = (current_index + 1) % len(self.kernal_sizes_array)

        # Update the button text to the next kernel size
        kernal_button.setText(self.kernal_sizes_array[next_index])

    def toggle_pass_filter(self):
        text = "Low Pass Filter" if self.pass_filter_button.text() == "High Pass Filter" else "High Pass Filter"
        self.pass_filter_button.setText(text)

    def setupImageGroupBoxes(self):
        """Creates two group boxes: Original Image & Processed Image."""
        self.original_groupBox, _ = self.util.createGroupBox(
            title="Original Image",
            size=QtCore.QSize(int(self.screen_size.width() * (502 / 1280)), int(self.screen_size.height() * (526 / 800))),
            style=self.groupbox_style,
            isGraph=False
        )
        self.processed_groupBox, _ = self.util.createGroupBox(
            title="Processed Image",
            size=QtCore.QSize(int(self.screen_size.width() * (502 / 1280)), int(self.screen_size.height() * (526 / 800))),
            style=self.groupbox_style,
            isGraph=False
        )

    def update_high_threshold(self, low_threshold_value):
        """
        Adjusts the high threshold based on changes in the low threshold to ensure it's always higher.
        """
        high_threshold_value = self.edge_detection_high_threshold_spinbox.value()
        if low_threshold_value >= high_threshold_value:
            new_high_value = low_threshold_value + 1
            self.edge_detection_high_threshold_spinbox.setValue(min(new_high_value, self.edge_detection_high_threshold_spinbox.maximum()))

    def update_low_threshold(self, high_threshold_value):
        """
        Adjusts the low threshold based on changes in the high threshold to ensure it's always lower.
        """
        low_threshold_value = self.edge_detection_low_threshold_spinbox.value()
        if high_threshold_value <= low_threshold_value:
            new_low_value = high_threshold_value - 1
            self.edge_detection_low_threshold_spinbox.setValue(max(new_low_value, self.edge_detection_low_threshold_spinbox.minimum()))

    # ----------------------------------------------------------------------
    # Retranslate
    # ----------------------------------------------------------------------
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    # ----------------------------------------------------------------------
    #  Show/Hide Logic
    # ----------------------------------------------------------------------
    def show_main_buttons(self):
        """Switch QStackedWidget to page 0 (main buttons)."""
        self.sidebar_stacked.setCurrentIndex(0)

    def show_noise_controls(self):
        """Switch QStackedWidget to page 1 (noise controls)."""
        self.sidebar_stacked.setCurrentIndex(1)

    def show_filter_controls(self):
        """Switch QStackedWidget to page 1 (noise controls)."""
        self.sidebar_stacked.setCurrentIndex(2)

    def show_edge_detection_controls(self):
        """Switch QStackedWidget to page 1 (noise controls)."""
        self.sidebar_stacked.setCurrentIndex(3)

    def show_refine_image_controls(self):
        self.sidebar_stacked.setCurrentIndex(4)

    def show_fourier_filter_controls(self):
        self.sidebar_stacked.setCurrentIndex(5)
