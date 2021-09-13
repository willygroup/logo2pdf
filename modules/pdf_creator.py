"""
Provides methods to create PDFs
"""

import os
import sys
import magic

from PyPDF2 import PdfFileWriter, PdfFileReader

from modules.utils import log


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

    def set_file_list(self, list):
        for file in list:
            if file.endswith(".pdf"):
                self.file_list.append(file)

    def process_files(self):
        n_files = 0
        for file in self.file_list:
            if self.checks_valid_pdf(file):
                input_file = file
                filename = os.path.basename(file)
                log("filename: " + filename)
                output_file = "{0}_{2}.{1}".format(*filename.rsplit(".", 1), "logo")

                output_file = os.path.join(self.output_dir, output_file)
                self.create_watermark(
                    input_pdf=input_file, output=output_file, watermark=self.logo_file
                )

                n_files = n_files + 1
        return n_files

    def create_watermark(self, input_pdf, output, watermark):
        watermark_obj = PdfFileReader(watermark)
        watermark_page = watermark_obj.getPage(0)

        try:
            pdf_reader = PdfFileReader(input_pdf)
            pdf_writer = PdfFileWriter()
        except:
            log("failed to initialize pdf_reader or writer")
            sys.exit(1)

        # Watermark all the pages
        for page in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page)
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)

        try:
            with open(output, "wb") as out:
                pdf_writer.write(out)
        except:
            log("Error writing to pdf output file")
            sys.exit(1)

        # remove the file only if reading from nologo directory
        if self.from_directory:
            os.remove(input_pdf)

    @staticmethod
    def checks_valid_pdf(input_file) -> bool:
        try:
            mime = magic.Magic(mime=True)
            mt = mime.from_file(input_file)
        except:
            return False
        else:
            if mt == "application/pdf":
                return True
        return False
