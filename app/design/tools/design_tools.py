from PyQt5 import QtCore, QtGui, QtWidgets


def adjust_quit_button(button):
    button.setMaximumSize(QtCore.QSize(50, 50))
    font = QtGui.QFont()
    font.setFamily("Hiragino Sans GB")
    font.setPointSize(40)
    font.setBold(True)
    font.setItalic(False)
    font.setUnderline(False)
    font.setWeight(75)
    font.setStrikeOut(False)
    font.setKerning(False)
    button.setFont(font)
    button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    button.setLayoutDirection(QtCore.Qt.LeftToRight)
    button.setMinimumSize(50, 50)
    button.setMaximumSize(50, 50)


def createButton(text, style, method=False, isVisible=True):
    button = QtWidgets.QPushButton()
    button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(style)
    button.setText(text)
    button.setMinimumSize(200, 50)
    button.setMaximumSize(200, 50)
    if not isVisible:
        button.hide()
    if method:
        button.clicked.connect(method)

    return button


def createGroupBox(title, size, style):
    groupBox = QtWidgets.QGroupBox()
    groupBox.setTitle(title)
    groupBox.setMinimumSize(size)
    groupBox.setMaximumSize(size)
    groupBox.setStyleSheet(style)
    return groupBox


def createSlider(min_value=0, max_value=100, initial_value=50, unit=None, style=False, isVisible=True):
    # Create a horizontal layout for the slider and label
    slider_layout = QtWidgets.QHBoxLayout()
    slider_layout.setContentsMargins(0, 0, 0, 0)
    slider_layout.setSpacing(10)

    # Create the slider
    slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    slider.setMinimum(min_value)
    slider.setMaximum(max_value)
    slider.setValue(initial_value)
    slider.setMaximumWidth(180)

    # Create the label
    unit_text = unit if unit is not None else ""
    label = QtWidgets.QLabel(f"{initial_value}{unit_text}")
    label.setMinimumWidth(20)
    label.setStyleSheet("color:white;")

    # Function to update the label based on the slider's value
    def updateLabel(value):
        label.setText(f"{value}%")

    # Connect the slider's valueChanged signal to update the label
    slider.valueChanged.connect(updateLabel)

    if style:
        slider.setStyleSheet(style)
    if not isVisible:
        slider.hide()
        label.hide()

    # Add the slider and label to the horizontal layout
    slider_layout.addWidget(slider)
    slider_layout.addWidget(label)

    return slider, label, slider_layout


def createSpinBox(min_value=0, max_value=100, initial_value=50, unit=None, style=False, isVisible=True):
    """
    Create a QSpinBox with a label that shows its value, optionally with a unit.

    Args:
    min_value (int): Minimum value of the spinbox.
    max_value (int): Maximum value of the spinbox.
    initial_value (int): Initial value of the spinbox.
    unit (str, optional): Unit to display next to the spinbox value. Defaults to None.
    style (str, optional): CSS style for the spinbox.
    isVisible (bool, optional): Whether the spinbox should be visible initially.

    Returns:
    QSpinBox, QLabel, QHBoxLayout: The created spinbox, label, and their layout.
    """
    # Create a horizontal layout for the spinbox and label
    spinbox_layout = QtWidgets.QHBoxLayout()
    spinbox_layout.setContentsMargins(0, 0, 0, 0)
    spinbox_layout.setSpacing(10)

    # Create the spinbox
    spinbox = QtWidgets.QSpinBox()
    spinbox.setMinimum(min_value)
    spinbox.setMaximum(max_value)
    spinbox.setValue(initial_value)
    spinbox.setMinimumWidth(180)
    spinbox.setMaximumWidth(180)

    # Create the label with or without a unit
    unit_text = unit if unit is not None else ""
    label = QtWidgets.QLabel(f"{initial_value}{unit_text}")
    label.setMinimumWidth(30)
    label.setStyleSheet("color: white;")

    # Function to update the label based on the spinbox's value
    def updateLabel(value):
        label.setText(f"{value}{unit_text}")

    # Connect the spinbox's valueChanged signal to update the label
    spinbox.valueChanged.connect(updateLabel)

    # Apply style if provided
    if style:
        spinbox.setStyleSheet(style)
    else:
        spinbox.setStyleSheet("color:white")

    # Control visibility
    if not isVisible:
        spinbox.hide()
        label.hide()

    # Add the spinbox and label to the horizontal layout
    spinbox_layout.addWidget(spinbox)
    spinbox_layout.addWidget(label)

    return spinbox, label, spinbox_layout


def createLabel(text, style=None, isVisible=True, isHead=False):
    """
    Create and return a QLabel with the specified properties, adjusting the font based on the label type.

    Args:
    text (str): The text to display in the label.
    style (str, optional): The CSS style string to apply to the label.
    isVisible (bool, optional): Whether the label should be visible initially.
    isHead (bool, optional): True if the label is a heading, False for body text.

    Returns:
    QtWidgets.QLabel: The created label.
    """
    label = QtWidgets.QLabel()
    label.setText(text)

    # Set font properties based on whether the label is a heading or body text
    font = QtGui.QFont()
    if isHead:
        font.setPointSize(24)  # Larger size for headings
        font.setBold(True)  # Bold for headings
        font.setItalic(False)  # Usually, headings are not italicized
    else:
        font.setPointSize(16)  # Smaller size for body text
        font.setBold(False)  # Not bold for body text
        font.setItalic(True)  # Italicize body text if needed

    label.setFont(font)

    # Apply the provided style or a default style if no style is provided
    if style:
        label.setStyleSheet(style)
    else:
        label.setStyleSheet("color: white;")  # Default color

    # Set visibility
    if not isVisible:
        label.hide()

    return label
