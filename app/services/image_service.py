import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog


class ImageServices:
    last_opened_folder = "static/images"

    @classmethod
    def upload_image_file(cls):
        """
        Opens a file dialog for the user to select an image file, and returns the path to the selected file.
        """
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(
                None,
                "Select Image File",
                cls.last_opened_folder,
                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)",
                options=options
            )

            # If a file is selected, update the last opened folder and return the file path
            if file_path:
                cls.last_opened_folder = os.path.dirname(file_path)
                return file_path
            else:
                print("No file was selected.")
                return None
        except Exception as e:
            raise Exception(f"An error occurred while uploading the file: {str(e)}")

    @staticmethod
    def set_image_in_groupbox(groupbox, image_path):
        label = QtWidgets.QLabel(groupbox)
        label.setPixmap(QtGui.QPixmap(image_path))
        label.setScaledContents(True)
        label.setMinimumSize(500, 500)
        label.setMaximumSize(groupbox.size())

        layout = groupbox.layout()
        if layout is None:
            # If the groupbox has no layout, create one and assign it
            layout = QtWidgets.QVBoxLayout(groupbox)
            groupbox.setLayout(layout)

        layout.addWidget(label)
        layout.setContentsMargins(0, 25, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignCenter)

    @staticmethod
    def clear_image(groupbox):
        layout = groupbox.layout()
        if layout:
            ImageServices.__clear_layout(layout)

    @staticmethod
    def __clear_layout(layout):
        """
        Recursively removes widgets and nested layouts from the given layout.
        """
        while layout.count():
            item = layout.takeAt(0)  # Take the item out of the layout

            widget = item.widget()
            if widget is not None:
                # If it's a widget, schedule it for deletion
                widget.deleteLater()
            else:
                sub_layout = item.layout()
                if sub_layout is not None:
                    # If it's a nested layout, recursively clear it
                    ImageServices.__clear_layout(sub_layout)

            # Here we do NOT call item.deleteLater() because item is a QLayoutItem, not a QWidget
            # Just let Python clean it up after the fact or do `del item`
            del item

    @staticmethod
    def _clear_sub_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                ImageServices._clear_sub_layout(item.layout())
            item.deleteLater()
