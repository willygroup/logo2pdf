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


def create_pdf_file(filename):
    shutil.copyfile(os.path.join(dirname, "test_files", "nologo_file.pdf"), filename)


def create_directory(pathname):
    os.makedirs(pathname, exist_ok=True)


def set_environment(dirname):
    reset_environment(dirname)
    create_directory(os.path.join(dirname, "tmp"))


def reset_environment(dirname):
    shutil.rmtree(os.path.join(dirname, "tmp"), ignore_errors=True)


class TestPdfCreatorMethods(unittest.TestCase):

    # TODO - Test  and process_files

    def test_init(self):
        pdf_creator = PdfCreator(dirname)

        self.assertEqual(
            pdf_creator.logo_file, os.path.join(dirname, "files", "logo.pdf")
        )
        self.assertEqual(pdf_creator.output_dir, os.path.join(dirname, "files", "logo"))
        self.assertEqual(
            pdf_creator.input_dir, os.path.join(dirname, "files", "nologo")
        )
        self.assertEqual(pdf_creator.file_list, [])
        self.assertEqual(pdf_creator.from_directory, False)

    def test_set_file_list(self):
        list = ["file1.pdf", "file2.pxf", "file3.pdf"]
        pdf_creator = PdfCreator(dirname)
        pdf_creator.set_file_list(list)

        expected = ["file1.pdf", "file3.pdf"]

        self.assertEqual(expected, pdf_creator.file_list)

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

        self.assertEqual(expected, pdf_creator.file_list)

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

    def test_process_files(self):
        set_environment(dirname)
        input_dir = os.path.join(dirname, "tmp", "nologo")
        output_dir = os.path.join(dirname, "tmp", "withlogo")
        file_1 = os.path.join(input_dir, "file1.pdf")
        file_2 = os.path.join(input_dir, "file2.pdf")
        file_3 = os.path.join(input_dir, "file3.pxf")
        file_4 = os.path.join(input_dir, "file4.pdf")

        file_1_out = os.path.join(output_dir, "file1_logo.pdf")
        file_2_out = os.path.join(output_dir, "file2_logo.pdf")
        file_3_out = os.path.join(output_dir, "file3_logo.pxf")
        file_4_out = os.path.join(output_dir, "file4_logo.pdf")

        logo_file = os.path.join(dirname, "test_files", "logo.pdf")

        create_directory(input_dir)
        create_directory(output_dir)
        create_pdf_file(file_1)
        create_pdf_file(file_2)
        create_pdf_file(file_3)
        create_pdf_file(file_4)

        pdf_creator = PdfCreator(dirname)

        pdf_creator.input_dir = os.path.join(input_dir)
        pdf_creator.output_dir = os.path.join(output_dir)
        pdf_creator.logo_file = logo_file
        pdf_creator.read_directory_content()

        pdf_creator.process_files()

        self.assertFalse(Path(file_1).exists())
        self.assertFalse(Path(file_2).exists())
        self.assertTrue(Path(file_3).exists())
        self.assertFalse(Path(file_4).exists())

        self.assertTrue(Path(file_1_out).exists())
        self.assertTrue(Path(file_2_out).exists())
        self.assertFalse(Path(file_3_out).exists())
        self.assertTrue(Path(file_4_out).exists())

        reset_environment(dirname)


if __name__ == "__main__":
    unittest.main()
