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
    window = MainWindow(dirname)
    window.show()
    app.exec_()


def execute_from_commandline():
    dirname = os.path.dirname(os.path.abspath(__file__))

    create_environment(dirname)

    pdf_creator = PdfCreator(dirname)

    if len(sys.argv) == 1:
        # process folder
        pdf_creator.read_directory_content()
    elif len(sys.argv) > 1:
        files = sys.argv
        files.remove(files[0])  # removing the executable file name
        pdf_creator.set_file_list(files)

    PROCESSED_FILES = pdf_creator.process_files()

    if PROCESSED_FILES > 0:
        print("{PROCESSED_FILES} files processed")
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
