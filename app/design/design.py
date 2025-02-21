from PyQt5 import QtCore, QtGui, QtWidgets
from app.design.tools.design_tools import (
    createButton,
    createGroupBox,
    createSlider,
    createLabel,
    adjust_quit_button
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        screen = QtWidgets.QApplication.primaryScreen().size()
        MainWindow.resize(screen.width(), screen.height())

        # 1) Define style variables
        self.setupStyles()

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
        self.title_icon.setPixmap(QtGui.QPixmap("static/images/icon.png"))
        self.title_icon.setScaledContents(True)
        self.title_icon.setObjectName("title_icon")

        self.title_label = createLabel(
            text="Pixelizing",
            style="color:white; padding:10px; padding-left:0;"
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
        self.upload_button = createButton("Upload", self.button_style)
        self.reset_image_button = createButton("Reset", self.button_style)
        self.save_image_button = createButton("Save", self.button_style)

        self.quit_app_button = createButton("X", self.quit_button_style)
        adjust_quit_button(self.quit_app_button)

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
        # plus a "Back" button at the bottom
        self.page_noise_layout.addWidget(self.back_button)
        self.page_noise_layout.addWidget(self.noise_mode_button)

        self.setupNoiseWidgets()

        self.sidebar_stacked.addWidget(self.page_noise_controls)

        # By default, show page 0
        self.sidebar_stacked.setCurrentIndex(0)

    def setupMainButtons(self):
        """
        Creates the main sidebar buttons list (Noise, Filters, etc.),
        plus sets up references so we can hide them if we want.
        """
        self.show_noise_options_button = createButton(
            "Noise", self.button_style, self.show_noise_controls
        )
        self.show_filter_options_button = createButton("Filters", self.button_style)
        self.show_edge_detecting_options_button = createButton("Edge Detector", self.button_style)
        self.show_metrics_button = createButton("View Metrics", self.button_style)
        self.show_refine_options_button = createButton("Refine Image", self.button_style)
        self.show_threshold_options_button = createButton("Thresholding", self.button_style)
        self.grayscaling_button = createButton("Gray Scaling", self.button_style)
        self.show_fourier_filter_options_button = createButton("Fourier Filters", self.button_style)
        self.upload_hybrid_image_button = createButton("Hybrid Image", self.button_style)

        # "Back" button used on the Noise page
        self.back_button = createButton("Back", self.button_style, self.show_main_buttons)
        self.noise_mode_button = createButton("Uniform Noise", self.button_style, self.toggle_noise_mode)

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

    def setupNoiseWidgets(self):
        """
        Creates the noise widgets (labels, sliders) and places them in page_noise_layout.
        """
        # Uniform Noise
        uniform_title = createLabel("Uniform Noise", "Color:white;", isVisible=True, isHead=True)
        self.page_noise_layout.addWidget(uniform_title)

        uniform_label = createLabel("Noise Amount", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(uniform_label)

        (self.uniform_noise_slider,
         uniform_slider_label,
         uniform_slider_layout) = createSlider(style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(uniform_slider_layout)

        # Gaussian Noise
        gaussian_title = createLabel("Gaussian Noise", "Color:white;", isVisible=True, isHead=True)
        self.page_noise_layout.addWidget(gaussian_title)

        mean_label = createLabel("Mean", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(mean_label)

        (self.mean_gaussian_noise_slider,
         mean_slider_label,
         mean_slider_layout) = createSlider(style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(mean_slider_layout)

        # This second label was "Mean" in your original code
        stddev_label = createLabel("Mean", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(stddev_label)

        (self.stddev_gaussian_noise_slider,
         stddev_val_label,
         stddev_layout) = createSlider(style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(stddev_layout)

        # Salt & Pepper Noise
        salt_pepper_noise_title = createLabel("Salt & Pepper Noise", "Color:white;", isVisible=True, isHead=True)
        self.page_noise_layout.addWidget(salt_pepper_noise_title)

        salt_pepper_noise_label = createLabel("Noise Amount", "Color:white;", isVisible=True)
        self.page_noise_layout.addWidget(salt_pepper_noise_label)

        (self.salt_pepper_noise_slider,
         uniform_slider_label,
         uniform_slider_layout) = createSlider(style=self.slider_style, isVisible=True)
        self.page_noise_layout.addLayout(uniform_slider_layout)

    def toggle_noise_mode(self):
        if self.noise_mode_button.text() == "Uniform Noise":
            self.noise_mode_button.setText("Gaussian Noise")
        elif self.noise_mode_button.text() == "Gaussian Noise":
            self.noise_mode_button.setText("Salt & Pepper Noise")
        else:
            self.noise_mode_button.setText("Uniform Noise")

    def setupImageGroupBoxes(self):
        """Creates two group boxes: Original Image & Processed Image."""
        self.original_groupBox = createGroupBox(
            title="Original Image",
            size=QtCore.QSize(500, 510),
            style=self.groupbox_style
        )
        self.processed_groupBox = createGroupBox(
            title="Processed Image",
            size=QtCore.QSize(500, 510),
            style=self.groupbox_style
        )

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
