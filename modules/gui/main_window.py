import os
from PySide2.QtWidgets import (
    QAction,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QLineEdit,
)
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
import modules
from modules.gui.drop_area import DropArea
from modules.lang import _
from modules.pdf_logo_creator import PdfLogoCreator, Point


class MainWindow(QMainWindow):
    def set_as_default(self):
        # TODO
        print("set_as_default")
        pass

    def create_logo_pdf(self):

        # TODO

        # TODO copy the image in the `files/default/images/` directory ?

        output_file = os.path.join(
            "files", "default", "pdfs", self.logo_settings_name.text()
        )

        # TODO checks on the fields
        _ = PdfLogoCreator.create_pdf_logo_creator(
            self.logo_image,
            output_file,
            Point(
                int(self.logo_settings_width.text()),
                int(self.logo_settings_height.text()),
            ),
            Point(
                float(self.logo_settings_pos_x.text()),
                float(self.logo_settings_pos_y.text()),
            ),
        )

        # TODO check if the pdflogcreator has successfully create a pdf
        pass

    def defaults_on_logo_settings(self):
        self.logo_settings_default.setText(_("Create PDF"))
        self.logo_settings_name.setText(_("logo_x"))
        self.logo_settings_width.setText(_("50"))
        self.logo_settings_height.setText(_("50"))
        self.logo_settings_pos_x.setText(_("10"))
        self.logo_settings_pos_y.setText(_("10"))

    def enable_logo_settings(self, status: bool):
        self.logo_settings_default.setDisabled(not status)
        self.logo_settings_name.setDisabled(not status)
        self.logo_settings_width.setDisabled(not status)
        self.logo_settings_height.setDisabled(not status)
        self.logo_settings_pos_x.setDisabled(not status)
        self.logo_settings_pos_y.setDisabled(not status)

    def logo_action(self, e):
        print(e.mimeData().text())
        image_url = e.mimeData().urls()[0].toLocalFile()
        # TODO Check that the file is a valid image
        self.logo_drop_area.set_background(image_url)
        self.logo_image = image_url

        self.enable_logo_settings(True)

    def __init__(self, dirname):
        super().__init__()

        self.dirname = dirname

        self.set_icon()
        self.create_menu()
        self.create_status_bar()

        main_layout = QHBoxLayout()

        pdf_drop_area = DropArea(_("Drag pdf files here!"), "pdf")
        pdf_drop_area.set_size(300, 300)
        pdf_drop_area.set_background_color("darkgrey")

        main_layout.addWidget(pdf_drop_area)

        right_layout = QVBoxLayout()

        self.logo_drop_area = DropArea(_("Drag a logo here"), "image")
        self.logo_drop_area.set_size(100, 100)
        self.logo_drop_area.set_background_color("red")

        self.logo_drop_area.set_action(self.logo_action)

        right_layout.addWidget(self.logo_drop_area)
        right_layout.setAlignment(self.logo_drop_area, Qt.AlignHCenter)

        self.logo_settings_default = QPushButton(_("Create PDF"))
        self.logo_settings_default.clicked.connect(self.create_logo_pdf)

        right_layout.addWidget(self.logo_settings_default)

        logo_settings_area = QGridLayout()

        logo_settings_area.addWidget(QLabel(_("Name:")), 0, 0)
        self.logo_settings_name = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings_name, 0, 1)
        # logo_settings_area.addWidget(QIcon(check_ok_filename), 1, 2)  # TODO

        logo_settings_area.addWidget(QLabel(_("Width:")), 1, 0)
        self.logo_settings_width = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings_width, 1, 1)
        logo_settings_area.addWidget(QLabel("[mm]"), 1, 2)

        logo_settings_area.addWidget(QLabel(_("Height:")), 2, 0)
        self.logo_settings_height = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings_height, 2, 1)
        logo_settings_area.addWidget(QLabel("[mm]"), 2, 2)

        logo_settings_area.addWidget(QLabel(_("Pos. X:")), 3, 0)
        self.logo_settings_pos_x = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings_pos_x, 3, 1)
        logo_settings_area.addWidget(QLabel("[mm]"), 3, 2)

        logo_settings_area.addWidget(QLabel(_("Pos. Y:")), 4, 0)
        self.logo_settings_pos_y = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings_pos_y, 4, 1)
        logo_settings_area.addWidget(QLabel("[mm]"), 4, 2)

        self.defaults_on_logo_settings()
        self.enable_logo_settings(False)

        right_layout.addLayout(logo_settings_area)

        main_layout.addLayout(right_layout)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def create_menu(
        self,
    ):
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu(_("File"))
        settings_menu = main_menu.addMenu(_("Settings"))
        help_menu = main_menu.addMenu(_("Help"))

        exitAction = QAction(
            QIcon(os.path.join("files", "images/exit.png")), _("Exit"), self
        )
        exitAction.setShortcut("Ctrl+X")

        exitAction.triggered.connect(self.exit_app)

        file_menu.addAction(exitAction)

        edit_settings = QAction(
            QIcon(os.path.join("files", "images/settings.png")), _("Edit"), self
        )
        settings_menu.addAction(edit_settings)
        # settings_menu.triggered.connect(self.edit_settings)

        aboutAction = QAction(
            QIcon(os.path.join("files", "images/info.png")), _("Info"), self
        )

        aboutAction.triggered.connect(self.show_about)
        help_menu.addAction(aboutAction)

    def exit_app(self):
        self.close()

    def show_about(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(_("About"))
        dlg.setText(
            f'<p style="text-align:center;"><big><b>{modules.__package_name__}</b></big></p>'
            f'<p style="text-align:right;"><i>{_("version")}:</i> {modules.__version__}<br/>'
            f'<i>{_("author")}:</i> willygroup@gmail.com<br/>'
        )
        dlg.show()

    # def edit_settings(self):
    #     settings_dialog = SettingsDialog(self)
    #     settings_dialog.draw(dirname, self.config)
    #     settings_dialog.show()

    def set_icon(self):
        appIcon = QIcon(os.path.join(self.dirname, "files", "images/icon.png"))
        self.setWindowIcon(appIcon)

    def create_status_bar(self):
        self.my_status = QStatusBar()
        self.my_status.showMessage(_("Ready"))
        self.setStatusBar(self.my_status)

    # def dragEnterEvent(self, e):
    #     if e.mimeData().hasUrls():
    #         e.acceptProposedAction()
