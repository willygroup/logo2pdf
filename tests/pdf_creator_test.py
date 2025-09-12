import os
import unittest
from pathlib import Path

from modules.paths import Paths
from modules.pdf_creator import PdfCreator
from tests.commons import (
    create_directory,
    create_logo_file,
    create_pdf_file,
    prepare_env,
    restore_env,
    test_directory,
)


class TestPdfCreatorMethods(unittest.TestCase):
    """
    Testing PdfCreator
    """

    def test_init(self):
        """
        Init method test
        """

        tmp_dir = prepare_env("pdf_creator_init")
        Paths.init(tmp_dir)
        try:
            pdf_creator = PdfCreator(os.path.join(test_directory, "logo.pdf"))

            self.assertEqual(
                pdf_creator.logo_file, os.path.join(test_directory, "logo.pdf")
            )
            self.assertEqual(pdf_creator.output_dir, Paths.out("logo"))
            self.assertEqual(
                pdf_creator.input_dir, os.path.join(tmp_dir, "output", "nologo")
            )
            self.assertEqual(pdf_creator.file_list, [])
            self.assertEqual(pdf_creator.from_directory, False)

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_set_file_list(self):
        """
        set_file method test
        """
        tmp_dir = prepare_env("pdf_creator_set_file_list")
        try:
            pdf_list = ["file1.pdf", "file2.pxf", "file3.pdf"]
            pdf_creator = PdfCreator(os.path.join(test_directory, "logo.pdf"))
            pdf_creator.set_file_list(pdf_list)

            expected = ["file1.pdf", "file3.pdf"]

            self.assertEqual(expected, pdf_creator.file_list)

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_read_directory_content(self):
        """
        read_directory_content method test
        """
        tmp_dir = prepare_env("pdf_creator_read_dir_content")

        try:
            # create 3 file on tmp directory
            create_pdf_file(os.path.join(tmp_dir, "file1.pdf"))
            create_pdf_file(os.path.join(tmp_dir, "file2.pxf"), False)
            create_pdf_file(os.path.join(tmp_dir, "file3.pdf"))
            pdf_creator = PdfCreator(os.path.join(test_directory, "logo.pdf"))
            # forcing input directory
            pdf_creator.input_dir = tmp_dir

            pdf_creator.read_directory_content()

            expected = [
                os.path.join(tmp_dir, "file3.pdf"),
                os.path.join(tmp_dir, "file1.pdf"),
            ]

            self.assertEqual(sorted(expected), sorted(pdf_creator.file_list))

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_create_watermark(self):
        """
        create_watermark method test
        """
        tmp_dir = prepare_env("pdf_creator_create_watermark")
        Paths.init(tmp_dir)

        try:
            input_pdf = os.path.join(tmp_dir, "nologo_file.pdf")
            output_pdf = os.path.join(tmp_dir, "logo_file.pdf")

            logo = os.path.join(test_directory, "test_files", "logo.pdf")

            create_pdf_file(input_pdf)

            pdf_creator = PdfCreator(os.path.join(test_directory, "logo.pdf"))
            pdf_creator.from_directory = True

            pdf_creator.create_watermark(input_pdf, output_pdf, logo)

            # outputfile does  exist
            self.assertTrue(Path(output_pdf).exists())

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_create_watermark_not_existing_logo(self):
        """
        create_watermark method test with no file
        """
        tmp_dir = prepare_env("pdf_creator_create_watermark_not_existing_logo")
        Paths.init(tmp_dir)

        try:
            input_pdf = os.path.join(tmp_dir, "nologo_file.pdf")
            output_pdf = os.path.join(tmp_dir, "logo_file.pdf")

            logo = os.path.join(tmp_dir, "invalid_logo.pdf")

            pdf_creator = PdfCreator(logo)
            pdf_creator.from_directory = True

            pdf_creator.create_watermark(input_pdf, output_pdf, logo)

            # outputfile does  exist
            self.assertFalse(Path(output_pdf).exists())

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_process_files(self):
        tmp_dir = prepare_env("pdf_creator_process_files")

        try:
            output_dir = os.path.join(tmp_dir, "withlogo")
            input_dir = os.path.join(tmp_dir, "no_logo")
            file_1 = os.path.join(input_dir, "file1.pdf")
            file_2 = os.path.join(input_dir, "file2.pdf")
            file_3 = os.path.join(input_dir, "file3.pxf")
            file_4 = os.path.join(input_dir, "file4.pdf")

            file_1_out = os.path.join(output_dir, "file1_logo.pdf")
            file_2_out = os.path.join(output_dir, "file2_logo.pdf")
            file_3_out = os.path.join(output_dir, "file3_logo.pxf")
            file_4_out = os.path.join(output_dir, "file4_logo.pdf")

            logo_file = os.path.join(tmp_dir, "logo.pdf")
            create_logo_file(logo_file)

            create_directory(input_dir)
            create_directory(output_dir)
            create_pdf_file(file_1)
            create_pdf_file(file_2, False)
            create_pdf_file(file_3, False)
            create_pdf_file(file_4)

            pdf_creator = PdfCreator(os.path.join(test_directory, "logo.pdf"))

            pdf_creator.input_dir = input_dir
            pdf_creator.output_dir = output_dir
            pdf_creator.logo_file = logo_file
            pdf_creator.read_directory_content()

            n_files = pdf_creator.process_files()

            self.assertTrue(n_files == 2)

            self.assertFalse(Path(file_1).exists())
            self.assertTrue(Path(file_2).exists())
            self.assertTrue(Path(file_3).exists())
            self.assertFalse(Path(file_4).exists())

            self.assertTrue(Path(file_1_out).exists())
            self.assertFalse(Path(file_2_out).exists())
            self.assertFalse(Path(file_3_out).exists())
            self.assertTrue(Path(file_4_out).exists())

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_checks_valid_pdf(self):
        tmp_dir = prepare_env("pdf_creator_checks_valid_pdf")

        try:
            file_1 = os.path.join(tmp_dir, "file1.pdf")
            file_2 = os.path.join(tmp_dir, "file2.pxf")
            file_3 = os.path.join(tmp_dir, "file3.pdf")

            create_pdf_file(file_1)
            create_pdf_file(file_2)
            create_pdf_file(file_3, False)

            self.assertTrue(PdfCreator.checks_valid_pdf(file_1))
            self.assertTrue(PdfCreator.checks_valid_pdf(file_2))
            self.assertFalse(PdfCreator.checks_valid_pdf(file_3))

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)


if __name__ == "__main__":
    unittest.main()
