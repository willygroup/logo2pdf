#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A script to add a watremark to a pdf file
"""

import os
import sys

from modules.utils import log
from modules.pdf_creator import PdfCreator


if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    dirname = sys._MEIPASS  # pylint: disable=no-member
else:
    dirname = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    # create directories

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
        log("%d files processed" % PROCESSED_FILES)
    else:
        log("No file processed")

# cSpell:ignore nologo
