#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
An app to add a watermark to pdf files
"""

import getopt
import os
import sys


from PySide2.QtWidgets import (
    QApplication,
)
from modules import utils
from modules.config import Config

from modules.gui.main_window import MainWindow
from modules.pdf_creator import PdfCreator
from modules.utils import create_environment


if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    dirname = sys._MEIPASS
else:
    dirname = os.path.dirname(os.path.abspath(__file__))


def main():

    app = QApplication(sys.argv)
    config = Config(dirname, os.path.join("files", "config.conf"))
    if config.load_config():
        window = MainWindow(dirname, config)
        window.show()
        app.exec_()
    else:
        print("Error loading the config")
        sys.exit(1)


def execute_from_commandline():
    """
    Execute the app as a script from commandline
    """
    create_environment(dirname)

    # TODO load logo from config
    logo_file = os.path.join("files", "logos", "willygroup.pdf")
    pdf_creator = PdfCreator(dirname, logo_file)

    if len(sys.argv) == 1:
        # process folder
        pdf_creator.read_directory_content()
    elif len(sys.argv) > 1:
        files = sys.argv
        files.remove(files[0])  # removing the executable file name
        pdf_creator.set_file_list(files)

    processed_files = pdf_creator.process_files()

    if processed_files > 0:
        print("{} files processed".format(processed_files))
        utils.open_directory(os.path.join("output", "logo"))
    else:
        print("No file processed")


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:", ["help", "headless"])
    except getopt.GetoptError:
        print("main.py --headless")
        sys.exit(2)
    if len(opts) > 0:
        for opt, arg in opts:
            if opt == "--headless":
                execute_from_commandline()
            else:
                print("main.py --headless")
                sys.exit()
    else:
        main()
