"""
Provides methods to create PDFs
"""

import os
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader

from modules.utils import log


def process_folder(dirname):
    """
    Process all the pdf files in the nologo directory
    """
    try:
        n_files = 0

        pdf_no_logo_directory = os.path.join(dirname, "files", "nologo")
        logo_file = os.path.join(dirname, "files", "logo.pdf")

        for file in os.listdir(pdf_no_logo_directory):
            if file.endswith(".pdf"):
                log(os.path.join(dirname, "files", "nologo", file))
                log(os.path.join(dirname, "files", "logo", file))
                o_filename = os.path.join(dirname, "files", "nologo", file)
                n_filename = os.path.join(dirname, "files", "logo", file)

                create_watermark(
                    input_pdf=o_filename, output=n_filename, watermark=logo_file
                )

                os.remove(o_filename)
                n_files = n_files + 1
    except FileExistsError():
        log("The file does not exist ")
        sys.exit(1)
    # // TODO: add more exceptions
    return n_files


def process_file_list(dirname, files):
    """
    Process a list of pdf files
    """
    logo_file = os.path.join(dirname, "files", "logo.pdf")
    n_files = 0
    for file in files:
        if file.endswith(".pdf"):
            log(os.path.join("./", file))
            o_filename = os.path.join("./", file)
            n_filename = os.path.join(dirname, "files/logo", file)

            create_watermark(
                input_pdf=o_filename, output=n_filename, watermark=logo_file
            )
            n_files = n_files + 1
    return n_files


def create_watermark(input_pdf, output, watermark):
    """
    Create the watermark
    """
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
