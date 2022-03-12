from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide2 import QtCore


class DropArea(QWidget):
    def __init__(self, text, mimetype="image"):
        super().__init__()
        if mimetype == "image":
            self.mimetype = ["image/png", "image/jpg", "image/jpeg"]
        else:
            self.mimetype = ["application/pdf"]
        layout = QVBoxLayout()
        layout.addWidget(QLabel(text))

        self.setLayout(layout)
        self.setAcceptDrops(True)

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    def set_background_color(self, color):
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: {}".format(color))

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        print("dropEvent")
        print(e.mimeData().text())
