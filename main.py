#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A script to add a watremark to a pdf file
"""

import os
import sys

from modules.utils import log
from modules.pdf_creator import process_file_list, process_folder


if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    dirname = sys._MEIPASS  # pylint: disable=no-member
else:
    dirname = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    # create directories

    if len(sys.argv) == 1:
        # process folder
        PROCESSED_FILES = process_folder(dirname)
    elif len(sys.argv) > 1:
        files = sys.argv
        files.remove(files[0])
        # list of pdf files
        PROCESSED_FILES = process_file_list(dirname, files)

    if PROCESSED_FILES > 0:
        log("%d files processed" % PROCESSED_FILES)
    else:
        log("No file processed")

# cSpell:ignore nologo
