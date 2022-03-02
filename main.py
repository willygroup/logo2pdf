#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A script to add a watermark to a pdf file
"""

from modules.utils import create_environment
import os
import sys

from modules.pdf_creator import PdfCreator

if __name__ == "__main__":
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
        print("%d files processed" % PROCESSED_FILES)
    else:
        print("No file processed")
