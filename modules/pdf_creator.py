"""
Provides methods to create PDFs
"""

from ast import Return
from codecs import ignore_errors
import os
import shutil
import sys

from PyPDF2 import PdfFileWriter, PdfFileReader
import PyPDF2


class PdfCreator:
    def __init__(self, dirname):
        self.dirname = dirname
        self.logo_file = os.path.join(dirname, "files", "logo.pdf")
        self.output_dir = os.path.join(self.dirname, "files", "logo")
        self.input_dir = os.path.join(self.dirname, "files", "nologo")
        self.file_list = []
        self.from_directory = False

    def read_directory_content(self):
        for file in os.listdir(self.input_dir):
            if file.endswith(".pdf"):
                self.file_list.append(os.path.join(self.input_dir, file))
        self.from_directory = True

    def set_file_list(self, file_list):
        for file in file_list:
            if file.endswith(".pdf"):
                self.file_list.append(file)

    def process_files(self) -> int:
        n_files = 0
        for file in self.file_list:

            input_file = file
            filename = os.path.basename(file)
            output_file = "{0}_{2}.{1}".format(*filename.rsplit(".", 1), "logo")

            output_file = os.path.join(self.output_dir, output_file)
            if self.create_watermark(
                input_pdf=input_file, output=output_file, watermark=self.logo_file
            ):

                n_files = n_files + 1
                # remove the file only if reading from nologo directory
                if self.from_directory:
                    os.remove(input_file)
                    # shutil.rmtree(input_file, ignore_errors=False)
                    # shutil.rmtree(input_file, ignore_errors=True)
        return n_files

    def create_watermark(self, input_pdf, output, watermark) -> bool:
        watermark_obj = PdfFileReader(watermark)
        watermark_page = watermark_obj.getPage(0)

        with open(input_pdf, "rb") as pdf:
            try:
                pdf_reader = PdfFileReader(pdf)
                pdf_writer = PdfFileWriter()
            except:
                print("failed to initialize pdf_reader or writer")
                return False

            # Watermark all the pages
            for page in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page)
                page.mergePage(watermark_page)
                pdf_writer.addPage(page)

            try:
                with open(output, "wb") as out:
                    pdf_writer.write(out)

            except:
                print("Error writing to pdf output file")
                return False
            return True
        return False

    @staticmethod
    def checks_valid_pdf(input_file) -> bool:
        try:
            PyPDF2.PdfFileReader(open(input_file, "rb"))
        except:
            return False
        else:
            return True
