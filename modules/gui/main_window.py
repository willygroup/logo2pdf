from dataclasses import dataclass
import os
import shutil

from PySide6.QtWidgets import (
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
    QCheckBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction

from modules import utils, __package_name__, __version__
from modules.config import Config
from modules.gui.drop_area import DropArea
from modules.lang import _
from modules.logo_metadata import LogoMetadata
from modules.paths import Paths
from modules.pdf_creator import PdfCreator
from modules.pdf_logo_creator import PdfLogoCreator, Point


@dataclass
class LogoSettings:
    name: QLineEdit
    aspect_ratio: QCheckBox
    width: QLineEdit
    height: QLineEdit
    default: QPushButton
    original_aspect_ratio: float
    pos_x: QLineEdit
    pos_y: QLineEdit

    def __init__(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self, config: Config):
        """
        App MainWindow
        """
        super().__init__()

        self.config = config
        self.logo_image = ""

        self.set_icon()
        self.create_menu()
        self.create_status_bar()

        main_layout = QHBoxLayout()

        self.pdf_drop_area = DropArea(_("Drag pdf files here!"), "pdf")
        self.pdf_drop_area.background.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pdf_drop_area.set_size(300, 300)
        self.pdf_drop_area.set_background_color("lightgrey")

        # TODO Create a background image
        # self.pdf_drop_area.set_background_image(QImage(Paths.image("dragpdf.png")))

        self.pdf_drop_area.set_action(self.add_logo)

        main_layout.addWidget(self.pdf_drop_area)

        right_layout = QVBoxLayout()
        label = QLabel("<i>" + _("Drag a logo (png) into the box below!") + "</i>")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        right_layout.addWidget(label)

        self.logo_drop_area = DropArea(_("Drag a logo here"), "image")
        self.logo_drop_area.set_size(100, 100)
        self.logo_drop_area.set_background_color("lightgrey")
        self.logo_drop_area.setStyleSheet("border :2px solid darkgrey;")

        self.logo_drop_area.set_action(self.logo_action)

        right_layout.addWidget(self.logo_drop_area)
        right_layout.setAlignment(self.logo_drop_area, Qt.AlignmentFlag.AlignHCenter)

        self.logo_settings = LogoSettings()

        self.logo_settings.default = QPushButton(_("Create PDF"))
        self.logo_settings.default.clicked.connect(self.create_logo_pdf)
        right_layout.addWidget(self.logo_settings.default)

        # TODO show created pdf
        self.logo_show_pdf = QPushButton(_("Show PDF Logo"))
        self.logo_show_pdf.clicked.connect(self.show_pdf_logo)
        self.logo_show_pdf.setEnabled(False)
        right_layout.addWidget(self.logo_show_pdf)

        logo_settings_area = QGridLayout()

        self.set_settings_area(logo_settings_area)

        self.set_default_logo()

        right_layout.addLayout(logo_settings_area)

        main_layout.addLayout(right_layout)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def set_settings_area(self, logo_settings_area: QGridLayout) -> None:
        row = 0

        logo_settings_area.addWidget(QLabel(_("Name:")), row, 0)
        self.logo_settings.name = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings.name, row, 1)
        row = row + 1

        logo_settings_area.addWidget(QLabel(_("Keep Aspect Ratio:")), row, 0)

        self.logo_settings.aspect_ratio = QCheckBox()
        logo_settings_area.addWidget(self.logo_settings.aspect_ratio)
        row = row + 1
        logo_settings_area.addWidget(QLabel(_("Width:")), row, 0)

        self.logo_settings.width = QLineEdit()
        self.logo_settings.width.textEdited.connect(
            lambda: self.calculate_aspect_ratio("width")
        )

        logo_settings_area.addWidget(self.logo_settings.width, row, 1)
        logo_settings_area.addWidget(QLabel("[mm]"), row, 2)
        row = row + 1

        logo_settings_area.addWidget(QLabel(_("Height:")), row, 0)
        self.logo_settings.height = QLineEdit()
        self.logo_settings.height.textEdited.connect(
            lambda: self.calculate_aspect_ratio("height")
        )
        logo_settings_area.addWidget(self.logo_settings.height, row, 1)
        logo_settings_area.addWidget(QLabel("[mm]"), row, 2)
        row = row + 1

        logo_settings_area.addWidget(QLabel(_("Pos. X:")), row, 0)
        self.logo_settings.pos_x = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings.pos_x, row, 1)
        logo_settings_area.addWidget(QLabel("[mm]"), row, 2)
        row = row + 1

        logo_settings_area.addWidget(QLabel(_("Pos. Y:")), row, 0)
        self.logo_settings.pos_y = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings.pos_y, row, 1)
        logo_settings_area.addWidget(QLabel("[mm]"), row, 2)

    def calculate_aspect_ratio(self, caller: str):
        print("caller: ", caller)
        if self.logo_settings.aspect_ratio.isChecked():
            if caller == "height":

                height = int(self.logo_settings.height.text())
                width = int(self.logo_settings.original_aspect_ratio * float(height))

            elif caller == "width":
                width = int(self.logo_settings.width.text())
                height = int(self.logo_settings.original_aspect_ratio * float(width))

            self.logo_settings.height.setText(f"{height:d}")
            self.logo_settings.width.setText(f"{width:d}")

    def show_pdf_logo(self):
        utils.open_directory(Paths.logos)

    def create_logo_pdf(self):
        """
        Create a pdf from the image dropped with the settings specified
        """

        output_file: str = str(self.logo_settings.name.text()) + ".pdf"
        output_file = Paths.logo(output_file)

        # TODO checks on the fields
        logo = PdfLogoCreator.create_pdf_logo_creator(
            self.logo_image,
            output_file,
            Point(
                int(self.logo_settings.width.text()),
                int(self.logo_settings.height.text()),
            ),
            Point(
                float(self.logo_settings.pos_x.text()),
                float(self.logo_settings.pos_y.text()),
            ),
        )

        # TODO check if the pdflogcreator has successfully create a pdf
        if logo:
            # Disable the settings, but the btn
            self.enable_logo_settings(False)
            self.logo_settings.default.setText(_("Set as Default"))
            self.logo_settings.default.setEnabled(True)
            self.logo_show_pdf.setEnabled(True)

            self.logo_settings.default.clicked.connect(
                lambda: self.set_default_logo(
                    self.logo_image, self.logo_settings.name.text()
                )
            )

    def set_logo_settings(
        self,
        btn_text: str,
        name: str,
        ar: bool,
        width: str,
        height: str,
        pos_x: str,
        pos_y: str,
    ):
        """
        Set the values for logo settings
        """
        self.logo_settings.default.setText(btn_text)
        self.logo_settings.name.setText(name)
        self.logo_settings.aspect_ratio.setChecked(ar)
        self.logo_settings.original_aspect_ratio = float(int(width) / int(height))
        self.logo_settings.width.setText(width)
        self.logo_settings.height.setText(height)
        self.logo_settings.pos_x.setText(pos_x)
        self.logo_settings.pos_y.setText(pos_y)

    def set_logo_settings_from_image(self, name, width, height):
        """
        Set the logo setting values from the data of the loaded image
        """
        # default width in mm:
        d_width = 40
        ratio = width / height
        d_height = int(d_width / ratio)

        self.set_logo_settings(
            _("Create PDF"), name, False, str(d_width), str(d_height), "10", "10"
        )

    def default_on_logo_settings(self):
        """
        Set the default value for logo settings
        """

        self.set_logo_settings(
            _("Create PDF"), _("name"), False, "50", "50", "10", "10"
        )

    def enable_logo_settings(self, status: bool):
        """
        Enable all the fields for the logo settings
        """
        self.logo_settings.default.setDisabled(not status)
        self.logo_settings.name.setDisabled(not status)
        self.logo_settings.aspect_ratio.setDisabled(not status)
        self.logo_settings.width.setDisabled(not status)
        self.logo_settings.height.setDisabled(not status)
        self.logo_settings.pos_x.setDisabled(not status)
        self.logo_settings.pos_y.setDisabled(not status)

    def add_logo(self, input_files):
        """
        Performs the add logo operation on the dropped files
        """
        # TODO check the file type
        # TODO read from self.default
        logo_file = os.path.join(Paths.logo(self.config.config_logo_name + ".pdf"))

        pdf_creator = PdfCreator(logo_file)

        file_list = []
        for file in input_files:
            file_list.append(file.toLocalFile())

        pdf_creator.set_file_list(file_list)

        processed_files = pdf_creator.process_files()

        if processed_files > 0:
            # TODO Write on Status Bar
            print(f"{processed_files} files processed")
            utils.open_directory(Paths.out("logo"))

        else:
            # TODO Write on Status Bar
            print("No file processed")

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

    def set_default_logo(
        self, image_logo_path: None | str = None, new_default_logo: None | str = None
    ):
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
            # Todo load default image data from json

        image_url = Paths.logo(image_name)

        if new_default_logo:
            self.config.set_config(new_default_logo)
            res = self.config.write_config()

            try:
                shutil.copyfile(str(image_logo_path), image_url)

                metadata = LogoMetadata(new_default_logo)

                metadata.set_name(new_default_logo)

                metadata.set_image_position(
                    int(self.logo_settings.pos_x.text()),
                    int(self.logo_settings.pos_y.text()),
                )
                metadata.set_image_size(
                    self.logo_settings.aspect_ratio.isChecked(),
                    int(self.logo_settings.width.text()),
                    int(self.logo_settings.height.text()),
                )
                if not metadata.store_metadata():
                    print("Error storing metadata")

            except shutil.SameFileError:
                # TODO Show a dialog with a same name warning
                self.enable_logo_settings(True)
                self.logo_settings.default.setText(_("Create PDF"))
                self.logo_settings.default.setEnabled(False)
            except Exception as ex:  # TODO HANDLE THIS
                print(f"Exception 1: {type(ex).__name__}")
                print(ex)

            self.logo_show_pdf.setEnabled(False)

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

        logo_path = Paths.image("icon.ico")

        dlg = QMessageBox(self)
        dlg.setWindowTitle(_("About"))
        dlg.setText(
            f'<img src="{logo_path}" width="50" height="50">'
            f'<p style="text-align:center;"><big><b>{__package_name__}</b></big></p>'
            f'<p style="text-align:right;"><i>{_("version")}:</i> {__version__}<br/>'
            f'<i>{_("author")}:</i> Daniele Forti (willygroup@gmail.com)<br/>'
        )
        dlg.show()

    # def edit_settings(self):
    #     settings_dialog = SettingsDialog(self)
    #     settings_dialog.draw( self.config)
    #     settings_dialog.show()

    def set_icon(self):
        """
        Sets the App icon
        """
        appIcon = QIcon(Paths.image("icon.png"))
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
