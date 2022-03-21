from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide2 import QtCore
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QMimeDatabase


class DropArea(QWidget):
    def __init__(self, text, mimetype="image"):
        super().__init__()
        if mimetype == "image":
            self.mimetypes = ["image/png", "image/jpg", "image/jpeg"]
        else:
            self.mimetypes = ["application/pdf"]
        layout = QVBoxLayout()
        self.background = QLabel(text)
        self.background.setStyleSheet("border :2px solid black;")
        self.background.setScaledContents(True)

        layout.addWidget(self.background)

        self.setLayout(layout)
        self.setAcceptDrops(True)

    def set_background_image(self, image_filename):
        self.background.setText("")
        pixmap = QPixmap(image_filename)
        self.background.setPixmap(pixmap)

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    def set_background_color(self, color):
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: {}".format(color))

    def find_type(self, mimedata):
        # TODO # FIXME
        urls = list()
        db = QMimeDatabase()
        for url in mimedata.urls():
            mimetype = db.mimeTypeForUrl(url)
            if mimetype.name() in self.mimetypes:
                urls.append(url)
        return urls

    def dragEnterEvent(self, event):
        print("formats: {}".format(event.mimeData().formats()))
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # TODO filter file type
        urls = self.find_type(event.mimeData())
        if len(urls) > 0:
            if self.action:
                event.accept()
                self.action(urls)

        event.ignore()

    def set_action(self, action):
        self.action = action
