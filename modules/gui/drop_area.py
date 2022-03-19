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
        self.background = QLabel(text)
        self.background.setStyleSheet("border :2px solid black;")

        layout.addWidget(self.background)

        self.setLayout(layout)
        self.setAcceptDrops(True)

    def set_background(self, image_filename):
        self.background.setText("")
        self.background.setStyleSheet(
            "border-image: url({}) 0 0 0 0 stretch stretch;".format(image_filename)
        )

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    def set_background_color(self, color):
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: {}".format(color))

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        print("dropEvent")
        # print(e.mimeData().text())
        if self.action:
            self.action(e)

    def set_action(self, action):
        self.action = action
