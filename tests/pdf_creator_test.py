import os
import shutil
import unittest
import tempfile
from pathlib import Path

from modules.pdf_creator import PdfCreator

dirname = os.path.realpath(__file__).replace("pdf_creator_test.py", "")


def create_file(filename):
    with open(filename, "w") as f:
        f.write("file: " + filename)


def set_environment(dirname):
    reset_environment(dirname)
    os.makedirs(os.path.join(dirname, "tmp"), exist_ok=True)


def reset_environment(dirname):
    shutil.rmtree(os.path.join(dirname, "tmp"), ignore_errors=True)


class TestPdfCreatorMethods(unittest.TestCase):

    # TODO - Test __init__ and process_files

    def test_set_file_list(self):
        list = ["file1.pdf", "file2.pxf", "file3.pdf"]
        pdf_creator = PdfCreator(dirname)
        pdf_creator.set_file_list(list)

        expected = ["file1.pdf", "file3.pdf"]

        self.assertEquals(expected, pdf_creator.file_list)

        reset_environment(dirname)

    def test_read_directory_content(self):
        set_environment(dirname)
        # create 3 file on tmp directory
        create_file(os.path.join(dirname, "tmp", "file1.pdf"))
        create_file(os.path.join(dirname, "tmp", "file2.pxf"))
        create_file(os.path.join(dirname, "tmp", "file3.pdf"))
        pdf_creator = PdfCreator(dirname)
        # forcing input directory
        pdf_creator.input_dir = os.path.join(dirname, "tmp")

        pdf_creator.read_directory_content()

        expected = [
            os.path.join(dirname, "tmp", "file1.pdf"),
            os.path.join(dirname, "tmp", "file3.pdf"),
        ]

        self.assertEquals(expected, pdf_creator.file_list)

        reset_environment(dirname)

    def test_create_watermark(self):
        set_environment(dirname)
        input_pdf = os.path.join(dirname, "tmp", "nologo_file.pdf")
        output_pdf = os.path.join(dirname, "tmp", "logo_file.pdf")
        logo = os.path.join(dirname, "test_files", "logo.pdf")
        shutil.copyfile(
            os.path.join(dirname, "test_files", "nologo_file.pdf"), input_pdf
        )

        pdf_creator = PdfCreator(dirname)
        pdf_creator.from_directory = True

        pdf_creator.create_watermark(input_pdf, output_pdf, logo)

        # inputfile does not exist
        self.assertFalse(Path(input_pdf).exists())
        # outputfile does not exist
        self.assertTrue(Path(output_pdf).exists())

        reset_environment(dirname)


if __name__ == "__main__":
    unittest.main()
