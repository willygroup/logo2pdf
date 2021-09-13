#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A script to add a watremark to a pdf file
"""

import os
import sys

from modules.utils import log
from modules.pdf_creator import PdfCreator

if __name__ == "__main__":
    dirname = os.path.dirname(os.path.abspath(__file__))

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