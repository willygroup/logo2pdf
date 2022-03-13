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


class MainWindow(QMainWindow):
    def set_as_default(self):
        print("set_as_default")
        pass

    def logo_action(self, e):
        print(e.mimeData().text())
        image_url = e.mimeData().urls()[0].toLocalFile()
        # TODO Check that the file is a valid image
        self.logo_drop_area.set_background(image_url)

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

        self.default_btn = QPushButton(_("Create PDF"))
        self.default_btn.setDisabled(True)
        self.default_btn.clicked.connect(self.set_as_default)

        right_layout.addWidget(self.default_btn)

        logo_settings_area = QGridLayout()

        logo_settings_area.addWidget(QLabel(_("Name:")), 0, 0)
        self.logo_settings_name = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings_name, 0, 1)
        self.logo_settings_name.setDisabled(True)
        # logo_settings_area.addWidget(QIcon(check_ok_filename), 1, 2)  # TODO

        logo_settings_area.addWidget(QLabel(_("Width:")), 1, 0)
        self.logo_settings_width = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings_width, 1, 1)
        self.logo_settings_width.setDisabled(True)
        logo_settings_area.addWidget(QLabel("[px]"), 1, 2)

        logo_settings_area.addWidget(QLabel(_("Height:")), 2, 0)
        self.logo_settings_height = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings_height, 2, 1)
        self.logo_settings_height.setDisabled(True)
        logo_settings_area.addWidget(QLabel("[px]"), 2, 2)

        logo_settings_area.addWidget(QLabel(_("Pos. X:")), 3, 0)
        self.logo_settings_pos_x = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings_pos_x, 3, 1)
        self.logo_settings_pos_x.setDisabled(True)
        logo_settings_area.addWidget(QLabel("[mm]"), 3, 2)

        logo_settings_area.addWidget(QLabel(_("Pos. Y:")), 4, 0)
        self.logo_settings_pox_y = QLineEdit()
        logo_settings_area.addWidget(self.logo_settings_pox_y, 4, 1)
        self.logo_settings_pox_y.setDisabled(True)
        logo_settings_area.addWidget(QLabel("[mm]"), 4, 2)

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
