#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A script to add a watremark to a pdf file 
"""

import os, sys, filetype, requests

from PyPDF2 import PdfFileWriter, PdfFileReader


if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    dirname = sys._MEIPASS
else:
    dirname = os.path.dirname(os.path.abspath(__file__))


debug_trace = True


def log(msg):
    if debug_trace:
        print(">>" + msg)


def create_watermark(input_pdf, output, watermark):
    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output, "wb") as out:
        pdf_writer.write(out)


def create_directories():
    if not os.path.exists("files"):
        os.makedirs("files")
    if not os.path.exists("files/nologo"):
        os.makedirs("files/nologo")
    if not os.path.exists("files/logo"):
        os.makedirs("files/logo")
    if not os.path.exists("files/logo.pdf"):
        log("No files/logo.pdf file found!")
        sys.exit(1)
    kind = filetype.guess(os.path.join(dirname, "files", "logo.pdf"))
    if kind is None or kind.mime != "application/pdf":
        log("logo.pdf is not a valid pdf file! mimetype: " + kind.mime)
        sys.exit(1)


def process_folder():

    try:
        n_files = 0

        pdf_no_logo_directory = os.path.join(dirname, "files", "nologo")
        logo_file = os.path.join(dirname, "files", "logo.pdf")

        for f in os.listdir(pdf_no_logo_directory):
            if f.endswith(".pdf"):
                log(os.path.join("files", "nologo", f))
                log(os.path.join("files", "logo", f))
                o_filename = os.path.join("files", "nologo", f)
                n_filename = os.path.join("files", "logo", f)

                create_watermark(
                    input_pdf=o_filename, output=n_filename, watermark=logo_file
                )

                os.remove(o_filename)
                n_files = n_files + 1
    except:
        log("An exception occurred ")
        sys.exit(1)
    return n_files


def process_file_list(files):
    n_files = 0
    for f in files:
        if f.endswith(".pdf"):
            log(os.path.join("./", f))
            o_filename = os.path.join("./", f)
            n_filename = os.path.join("files/logo", f)

            create_watermark(
                input_pdf=o_filename, output=n_filename, watermark="files/logo.pdf"
            )
            n_files = n_files + 1
    return n_files


if __name__ == "__main__":
    # create directories
    create_directories()

    if len(sys.argv) == 1:
        # process folder
        processed_files = process_folder()
    elif len(sys.argv) > 1:
        files = sys.argv
        files.remove(files[0])
        # list of pdf files
        processed_files = process_file_list(files)

    if processed_files > 0:
        log("%d files processed" % processed_files)
    else:
        log("No file processed")

# cSpell:ignore nologo
