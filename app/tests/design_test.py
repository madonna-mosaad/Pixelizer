from PyQt5 import QtCore, QtGui, QtWidgets
from app.design.tools.design_tools import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        # Obtain screen resolution and adjust window size dynamically
        screen = QtWidgets.QApplication.primaryScreen().size()
        MainWindow.resize(screen.width(), screen.height())

        self.button_style = """
        QPushButton {
            background-color: rgb(30, 30, 30);
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
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

        self.main_window_style = """
        background-color: #040d12;
        """

        MainWindow.setStyleSheet(self.main_window_style)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # --------------------------
        # TOP-LEVEL LAYOUTS (REMOVED THE QGridLayout)
        # --------------------------
        # 1) A vertical layout to hold navbar on top and main content below
        self.main_vertical_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.main_vertical_layout.setSpacing(0)
        self.main_vertical_layout.setObjectName("main_vertical_layout")

        # 2) A horizontal layout in which:
        #    - Left side: sidebar
        #    - Middle/Right: original image box and processed image box
        self.main_content_layout = QtWidgets.QHBoxLayout()
        self.main_content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_content_layout.setSpacing(10)
        self.main_content_layout.setObjectName("main_content_layout")

        MainWindow.setCentralWidget(self.centralwidget)

        # Menu bar and status bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, screen.width(), 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Setup Sidebar and Navbar (now they create class-level layouts)
        self.setupSidebar()
        self.setupNavbar()

        # --------------------------
        # CREATE GROUP BOXES
        # --------------------------
        self.processed_image_groupBox = createGroupBox(
            "Processed Image", QtCore.QSize(505, 560), self.groupbox_style
        )
        self.original_image_groupBox = createGroupBox(
            "Original Image", QtCore.QSize(505, 560), self.groupbox_style
        )

        # --------------------------
        # ADD WIDGETS/ LAYOUTS TO OUR MAIN LAYOUTS
        # --------------------------
        # Add navbar_layout on top in the vertical layout
        self.main_vertical_layout.addLayout(self.navbar_layout)

        # Add sidebar on the left
        self.main_content_layout.addLayout(self.sidebar_layout)

        # A horizontal layout for the two group boxes
        self.images_layout = QtWidgets.QHBoxLayout()
        self.images_layout.setSpacing(10)
        self.images_layout.setObjectName("images_layout")

        self.images_layout.addWidget(self.original_image_groupBox)
        self.images_layout.addWidget(self.processed_image_groupBox)

        # Add the images layout to the main_content_layout (to the right of sidebar)
        self.main_content_layout.addLayout(self.images_layout)

        # Finally add main_content_layout to the vertical layout
        self.main_vertical_layout.addLayout(self.main_content_layout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # -----------------------------------------------
    # NAVBAR
    # -----------------------------------------------
    def setupNavbar(self):
        self.navbar_layout = QtWidgets.QHBoxLayout()
        self.navbar_layout.setSpacing(25)
        self.navbar_layout.setObjectName("navbar_layout")

        # Navbar components
        self.title_icon = QtWidgets.QLabel()
        self.title_icon.setMaximumSize(QtCore.QSize(80, 80))
        self.title_icon.setPixmap(QtGui.QPixmap("static/images/icon.png"))
        self.title_icon.setScaledContents(True)
        self.title_icon.setObjectName("title_icon")

        self.title_label = QtWidgets.QLabel()
        self.title_label.setMaximumSize(QtCore.QSize(160, 100))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(True)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color:white;")
        self.title_label.setObjectName("title_label")

        title_layout = QtWidgets.QHBoxLayout()
        title_layout.addWidget(self.title_icon)
        title_layout.addWidget(self.title_label)
        self.navbar_layout.addLayout(title_layout)

        # Navbar buttons
        self.upload_button = createButton("Upload", self.button_style)
        self.reset_image_button = createButton("Reset", self.button_style)
        self.save_image_button = createButton("Save", self.button_style)
        self.quit_app_button = createButton("X", self.quit_button_style)
        adjust_quit_button(self.quit_app_button)

        self.navbar_layout.addWidget(self.upload_button)
        self.navbar_layout.addWidget(self.reset_image_button)
        self.navbar_layout.addWidget(self.save_image_button)
        self.navbar_layout.addWidget(self.quit_app_button)

    # -----------------------------------------------
    # SIDEBAR
    # -----------------------------------------------
    def setupSidebar(self):
        self.sidebar_layout = QtWidgets.QVBoxLayout()
        self.sidebar_layout.setSpacing(25)
        self.sidebar_layout.setObjectName("sidebar_layout")

        self.setupSidebarButtons()
        self.setupNoiseWidgets()

        # All noise-related widgets that get shown/hidden
        self.controller_widgets = [
            self.uniform_noise_title,
            self.uniform_noise_label,
            self.uniform_noise_slider,
            self.uniform_noise_slider_label,
            self.gaussian_noise_title,
            self.mean_gaussian_noise_label,
            self.mean_gaussian_noise_slider,
            self.mean_gaussian_slider_label,
            self.standarad_deviation_gaussian_noise_label,
            self.standarad_deviation_gaussian_noise_slider,
            self.standarad_deviation_gaussian_noise_label
        ]

    def setupSidebarButtons(self):
        self.back_button = createButton("Back", self.button_style, self.show_main_buttons, False)
        self.sidebar_layout.addWidget(self.back_button)

        # Sidebar buttons
        self.show_noise_options_button = createButton("Noise", self.button_style, self.show_noise_controls, True)
        self.show_filter_options_button = createButton("Filters", self.button_style)
        self.show_edge_detecting_options_button = createButton("Edge Detector", self.button_style)
        self.show_metrics_button = createButton("View Metrics", self.button_style)
        self.show_refine_options_button = createButton("Refine Image", self.button_style)
        self.show_threshold_options_button = createButton("Thresholding", self.button_style)
        self.grayscaling_button = createButton("Gray Scaling", self.button_style)
        self.show_fourier_filter_options_button = createButton("Fourier Filters", self.button_style)
        self.upload_hybrid_image_button = createButton("Hybrid Image", self.button_style)

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
        for button in self.MAIN_BUTTONS:
            self.sidebar_layout.addWidget(button)

    def setupNoiseWidgets(self):
        self.uniform_noise_title = createLabel("Uniform Noise", "Color:white;", isVisible=False)
        self.uniform_noise_label = createLabel("Noise Amount", "Color:white;", isVisible=False)
        self.uniform_noise_slider, self.uniform_noise_slider_label, self.uniform_noise_layout = createSlider(
            style=self.slider_style, isVisible=False
        )
        self.sidebar_layout.addWidget(self.uniform_noise_title)
        self.sidebar_layout.addWidget(self.uniform_noise_label)
        self.sidebar_layout.addLayout(self.uniform_noise_layout)

        self.gaussian_noise_title = createLabel("Gaussian Noise", "Color:white;", isVisible=False)
        self.mean_gaussian_noise_label = createLabel("Mean", "Color:white;", isVisible=False)
        self.mean_gaussian_noise_slider, self.mean_gaussian_slider_label, self.mean_gaussian_noise_layout = createSlider(
            style=self.slider_style, isVisible=False
        )
        self.sidebar_layout.addWidget(self.gaussian_noise_title)
        self.sidebar_layout.addWidget(self.mean_gaussian_noise_label)
        self.sidebar_layout.addLayout(self.mean_gaussian_noise_layout)

        # Note: Label text was "Mean" twice; keeping your code but you may want to rename it
        self.standarad_deviation_gaussian_noise_label = createLabel("Mean", "Color:white;", isVisible=False)
        self.standarad_deviation_gaussian_noise_slider, self.standarad_deviation_gaussian_noise_label, self.standarad_deviation_gaussian_noise_layout = createSlider(
            style=self.slider_style, isVisible=False
        )

        self.sidebar_layout.addWidget(self.standarad_deviation_gaussian_noise_label)
        self.sidebar_layout.addLayout(self.standarad_deviation_gaussian_noise_layout)

    # -----------------------------------------------
    # RETRANSLATE & UTILITY METHODS
    # -----------------------------------------------
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_label.setText(_translate("MainWindow", "Pixelizing"))

    def hide_main_buttons(self):
        for button in self.MAIN_BUTTONS:
            button.hide()
        self.back_button.show()

    def show_main_buttons(self):
        for button in self.MAIN_BUTTONS:
            button.show()
        self.back_button.hide()
        self.hide_widgets(self.controller_widgets)

    def hide_widgets(self, widgets_array):
        for widget in widgets_array:
            widget.hide()

    def show_widgets(self, widgets_array):
        for widget in widgets_array:
            widget.show()

    def show_noise_controls(self):
        self.hide_main_buttons()
        self.show_widgets(self.controller_widgets)
