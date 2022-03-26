import os
import shutil
import modules

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
from modules import utils
from modules.config import Config
from modules.gui.drop_area import DropArea
from modules.lang import _
from modules.logo_metadata import LogoMetadata
from modules.pdf_creator import PdfCreator
from modules.pdf_logo_creator import PdfLogoCreator, Point


class MainWindow(QMainWindow):
    def __init__(self, dirname, config: Config):
        """
        App MainWindow
        """
        super().__init__()

        self.dirname = dirname
        self.config = config

        self.set_icon()
        self.create_menu()
        self.create_status_bar()

        main_layout = QHBoxLayout()

        self.pdf_drop_area = DropArea(_("Drag pdf files here!"), "pdf")
        self.pdf_drop_area.set_size(300, 300)
        self.pdf_drop_area.set_background_color("darkgrey")
        self.pdf_drop_area.set_action(self.add_logo)

        main_layout.addWidget(self.pdf_drop_area)

        right_layout = QVBoxLayout()

        self.logo_drop_area = DropArea(_("Drag a logo here"), "image")
        self.logo_drop_area.set_size(100, 100)
        self.logo_drop_area.set_background_color("lightgrey")
        self.logo_drop_area.setStyleSheet("border :2px solid darkgrey;")

        self.logo_drop_area.set_action(self.logo_action)

        right_layout.addWidget(self.logo_drop_area)
        right_layout.setAlignment(self.logo_drop_area, Qt.AlignHCenter)

        self.logo_settings_default = QPushButton(_("Create PDF"))
        self.logo_settings_default.clicked.connect(self.create_logo_pdf)
        right_layout.addWidget(self.logo_settings_default)

        # TODO show created pdf
        self.logo_show_pdf = QPushButton(_("Show PDF"))
        # self.logo_show_pdf.clicked.connect(self.show_pdf)
        self.logo_show_pdf.setVisible(False)
        right_layout.addWidget(self.logo_show_pdf)

        logo_settings_area = QGridLayout()

        logo_settings_area.addWidget(QLabel(_("Name:")), 0, 0)
        self.logo_settings_name = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings_name, 0, 1)

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

        self.set_default_logo()

        right_layout.addLayout(logo_settings_area)

        main_layout.addLayout(right_layout)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def create_logo_pdf(self):
        """
        Create a pdf from the image dropped with the settings specified
        """

        output_file: str = str(self.logo_settings_name.text()) + ".pdf"
        output_file = os.path.join("files", "logos", output_file)

        # TODO checks on the fields
        logo = PdfLogoCreator.create_pdf_logo_creator(
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
        if logo:
            # Disable the settings, but the btn
            self.enable_logo_settings(False)
            self.logo_settings_default.setText(_("Set as Default"))
            self.logo_settings_default.setEnabled(True)
            self.logo_show_pdf.setVisible(True)

            self.logo_settings_default.clicked.connect(
                lambda: self.set_default_logo(
                    self.logo_image, self.logo_settings_name.text()
                )
            )

    def set_logo_settings_from_image(self, name, width, heigth):
        """
        Set the logo setting values from the data of the loaded image
        """
        # default width in mm:
        d_width = 40
        ratio = width / heigth
        d_heigth = int(d_width / ratio)

        self.logo_settings_default.setText(_("Create PDF"))
        self.logo_settings_name.setText(name)
        self.logo_settings_width.setText(str(d_width))
        self.logo_settings_height.setText(str(d_heigth))
        self.logo_settings_pos_x.setText(_("10"))
        self.logo_settings_pos_y.setText(_("10"))

    def default_on_logo_settings(self):
        """
        Set the default value for logo settings
        """
        self.logo_settings_default.setText(_("Create PDF"))
        self.logo_settings_name.setText(_("name"))
        self.logo_settings_width.setText(_("50"))
        self.logo_settings_height.setText(_("50"))
        self.logo_settings_pos_x.setText(_("10"))
        self.logo_settings_pos_y.setText(_("10"))

    def enable_logo_settings(self, status: bool):
        """
        Enable all the fields for the logo settings
        """
        self.logo_settings_default.setDisabled(not status)
        self.logo_settings_name.setDisabled(not status)
        self.logo_settings_width.setDisabled(not status)
        self.logo_settings_height.setDisabled(not status)
        self.logo_settings_pos_x.setDisabled(not status)
        self.logo_settings_pos_y.setDisabled(not status)

    def add_logo(self, input_files):
        """
        Performs the add logo operation on the dropped files
        """
        # TODO check the file type
        # TODO read from self.default
        logo_file = os.path.join(
            "files", "logos", self.config.config_logo_name + ".pdf"
        )

        pdf_creator = PdfCreator(self.dirname, logo_file)

        file_list = []
        for file in input_files:
            file_list.append(file.toLocalFile())

        pdf_creator.set_file_list(file_list)

        processed_files = pdf_creator.process_files()

        if processed_files > 0:
            print("{} files processed".format(processed_files))
            # TODO Open the output directory
            utils.open_directory(os.path.join("output", "logo"))

        else:
            print("No file processed")

        pass

    def logo_action(self, urls):
        """
        Set as image of the logo the image dropped
        """
        # TODO Check that the file is a valid image
        width = 40
        height = 40
        image_url = urls[0].toLocalFile()
        res = self.logo_drop_area.set_background_image(image_url)
        if res:
            width = res[0]
            height = res[1]
        self.logo_image = image_url
        self.set_logo_settings_from_image(
            os.path.splitext(os.path.basename(image_url))[0], width, height
        )

        self.enable_logo_settings(True)

    def set_default_logo(self, image_logo_path=None, new_default_logo=None):
        """
        Set the default logo
        """

        width = 50
        height = 50

        if new_default_logo:
            image_name = new_default_logo + ".png"
            self.config.config_logo_name = new_default_logo
        else:
            image_name = self.config.config_logo_name + ".png"
            # Todo load default data from json

        image_url = os.path.join(self.dirname, "files", "logos", image_name)

        if new_default_logo:
            self.config.set_config(new_default_logo)
            res = self.config.write_config()

            try:
                shutil.copyfile(image_logo_path, image_url)

                metadata = LogoMetadata(self.dirname, new_default_logo)

                metadata.set_name(new_default_logo)

                metadata.set_image_position(
                    float(self.logo_settings_pos_x.text()),
                    float(self.logo_settings_pos_y.text()),
                )
                metadata.set_image_size(
                    int(self.logo_settings_width.text()),
                    int(self.logo_settings_height.text()),
                )
                if not metadata.store_metadata():
                    print("Error storing metadata")

            except shutil.SameFileError:
                # TODO Show a dialog with a same name warning
                self.enable_logo_settings(True)
                self.logo_settings_default.setText(_("Create PDF"))
                self.logo_settings_default.setEnabled(False)

                pass
            except Exception as ex:
                print("Exception: {}".format(type(ex).__name__))

            self.logo_show_pdf.setVisible(False)

        # TODO Check that the file is a valid image
        res = self.logo_drop_area.set_background_image(image_url)
        if res:
            width = res[0]
            height = res[1]

        self.set_logo_settings_from_image(self.config.config_logo_name, width, height)
        self.enable_logo_settings(False)

    def create_menu(
        self,
    ):
        """
        Creates the App menu
        """
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
        """
        Exits the App
        """
        self.close()

    def show_about(self):
        """
        Shows the About dialog
        """

        logo_path = os.path.join(self.dirname, "files", "images", "icon.ico")

        dlg = QMessageBox(self)
        dlg.setWindowTitle(_("About"))
        dlg.setText(
            f'<img src="{logo_path}" width="50" height="50">'
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
        """
        Sets the App icon
        """
        appIcon = QIcon(os.path.join(self.dirname, "files", "images/icon.png"))
        self.setWindowIcon(appIcon)

    def create_status_bar(self):
        """
        Creates the App Status bar
        """
        self.my_status = QStatusBar()
        self.my_status.showMessage(_("Ready"))
        self.setStatusBar(self.my_status)

    # def dragEnterEvent(self, e):
    #     if e.mimeData().hasUrls():
    #         e.acceptProposedAction()
