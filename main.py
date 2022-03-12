#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
An app to add a watermark to pdf files
"""

import os
import logging
import sys
import modules
import gettext
import locale

from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)
from PySide2.QtGui import QIcon
from functools import partial
from PySide2 import QtCore


if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    dirname = sys._MEIPASS
else:
    dirname = os.path.dirname(os.path.abspath(__file__))


current_locale, _ = locale.getlocale()
if current_locale == "Italian_Italy":
    current_locale = "it_IT"
locale_path = os.path.join("files", "locale")
dictionary = gettext.translation("csv2lbl", locale_path, [current_locale])
dictionary.install()
_ = dictionary.gettext


class ErrorBox:
    def __init__(self, parent, title, message):
        msg = QMessageBox(parent)
        flags = QtCore.Qt.Dialog
        flags |= QtCore.Qt.CustomizeWindowHint
        flags |= QtCore.Qt.WindowTitleHint
        msg.setWindowFlags(flags)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        config, csv_config = self.load_config()

        self.config = config
        self.csv_config = csv_config

        self.setAcceptDrops(True)
        self.setWindowTitle("csv2lbl")
        self.setGeometry(300, 200, 500, 400)

        self.label = QLabel(_("Drag&Drop csv files here..."))

        self.label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.label.setStyleSheet(
            " font-size: 20px; font-weight: bold; font-family: Courier New;"
        )

        self.set_icon()
        self.create_menu()
        self.create_status_bar()

        self.row = self.create_button(_("Single Label Sheet for Row"), "row.png", 0)
        self.row.setCheckable(True)
        self.order = self.create_button(
            _("Single Labels sheet for order"), "order.png", 1
        )
        self.order.setCheckable(True)
        self.all = self.create_button(_("Single Labels Sheet for all"), "all.png", 2)
        self.all.setCheckable(True)

        self.row.clicked.connect(partial(self.set_pdf_creation_flag, 0))
        self.order.clicked.connect(partial(self.set_pdf_creation_flag, 1))
        self.all.clicked.connect(partial(self.set_pdf_creation_flag, 2))

        buttons_group = QButtonGroup(self)
        buttons_group.addButton(self.row)
        buttons_group.addButton(self.order)
        buttons_group.addButton(self.all)

        self.set_label()

        button_bar = QWidget(self)
        button_bar_layout = QHBoxLayout()
        button_bar_layout.addWidget(self.row)
        button_bar_layout.addWidget(self.order)
        button_bar_layout.addWidget(self.all)

        button_bar.setLayout(button_bar_layout)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(button_bar)

        main_widget = QWidget(self)
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)
        self.setFixedSize(450, 350)

    def create_button(self, tooltip_text: str, image_filename: str, value: int):
        button = QPushButton()
        button.setToolTip(tooltip_text)
        button.setIcon(QIcon(os.path.join("files", "images", image_filename)))
        button.setIconSize(QtCore.QSize(100, 100))
        button.setFixedSize(110, 110)
        button.setCheckable(True)
        button.clicked.connect(partial(self.set_pdf_creation_flag, value))
        return button

    def set_pdf_creation_flag(self, value):
        self.config.pdf_creation = int(value)

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
        settings_menu.triggered.connect(self.edit_settings)

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
            f"<i>Copyright 2022:</i> Daniele Forti"
        )
        dlg.show()

    def edit_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.draw(dirname, self.config)
        settings_dialog.show()

    def set_icon(self):
        appIcon = QIcon(os.path.join(dirname, "files", "images/icon.png"))
        self.setWindowIcon(appIcon)

    def create_status_bar(self):
        self.my_status = QStatusBar()
        self.my_status.showMessage(_("Ready"))
        self.setStatusBar(self.my_status)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        self.my_status.showMessage(_("In progress..."))

        pdf_output_type = int(self.config.pdf_creation)
        csv_config = self.csv_config
        os_name = self.config.os_name
        libreoffice_exe = self.config.libreoffice_exe
        pdftk_exe = self.config.pdftk_exe
        file_list = e.mimeData().urls()

        labels_no = Utils.create_pdf_labels(
            file_list,
            dirname,
            csv_config,
            pdf_output_type,
            os_name,
            libreoffice_exe,
            pdftk_exe,
        )

        if labels_no < 0:
            self.my_status.showMessage(
                _("Error creating the labels...").format(labels_no), 3000
            )
            ErrorBox(
                self,
                _("Error!"),
                _(
                    "Cannot create the labels,\nplease close all the labels viewer opened!"
                ),
            )
            return

        # update the status bar
        self.my_status.showMessage(
            _("Done! Created {} labels...").format(labels_no), 3000
        )


def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


# if __name__ == "__main__":

#     FORMAT = "%(asctime)-15s `%(name)s` => '%(message)s'"
#     logging.basicConfig(
#         filename="./files/csv2lbl.log", level=logging.INFO, format=FORMAT
#     )
#     logger = logging.getLogger("main")

#     logger.info("App Started")

#     if not Utils.check_if_template_exists(
#         os.path.join(dirname, "files", "template.rtf")
#     ):
#         logger.error(
#             "Abort: template file {} doesn't exist!".format(
#                 os.path.join(dirname, "files", "template.rtf")
#             )
#         )
#         sys.exit(1)

#     main()

#     logger.info("App Closed")

#     sys.exit(0)


# #! /usr/bin/env python
# # -*- coding: utf-8 -*-

# """
# A script to add a watermark to a pdf file
# """

# import os
# import sys

# from modules.utils import create_environment
# from modules.pdf_creator import PdfCreator

# if __name__ == "__main__":
#     dirname = os.path.dirname(os.path.abspath(__file__))

#     create_environment(dirname)

#     pdf_creator = PdfCreator(dirname)

#     if len(sys.argv) == 1:
#         # process folder
#         pdf_creator.read_directory_content()
#     elif len(sys.argv) > 1:
#         files = sys.argv
#         files.remove(files[0])  # removing the executable file name
#         pdf_creator.set_file_list(files)

#     PROCESSED_FILES = pdf_creator.process_files()

#     if PROCESSED_FILES > 0:
#         print("{PROCESSED_FILES} files processed")
#     else:
#         print("No file processed")
