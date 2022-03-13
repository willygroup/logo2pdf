import unittest


from modules.pdf_logo_creator import PdfLogoCreator, Point

from tests.common import (
    prepare_env,
    restore_env,
    dirname,
)

import os


class TestPdfLogoCreatorMethods(unittest.TestCase):
    """
    Testing PdfLogoCreator
    """

    def test_pdflogocreator_init(self):
        """
        Init method test
        """

        tmp_dir = prepare_env("pdflogocreator")

        image_file = os.path.join(dirname, "test_files", "image_logo.png")
        output_file = os.path.join(tmp_dir, "test.pdf")

        pdf_logo = PdfLogoCreator(
            image_file,
            output_file,
            Point(50, 50),
            Point(6, 6),
        )

        # check if the file exist
        try:
            self.assertIsNotNone(pdf_logo)
            self.assertTrue(os.path.exists(output_file))
        finally:
            restore_env(tmp_dir)

    def test_pdflogocreator_not_existent_image(self):
        """
        create_pdf_logo_creator test with not existent image
        """

        tmp_dir = prepare_env("pdflogocreator_not_existent")

        image_file = os.path.join(tmp_dir, "image_logo.png")
        output_file = os.path.join(tmp_dir, "test.pdf")

        pdf_logo = PdfLogoCreator.create_pdf_logo_creator(
            image_file,
            output_file,
            Point(50, 50),
            Point(6, 6),
        )

        # check if the file exist
        try:
            self.assertIsNone(pdf_logo)
            self.assertFalse(os.path.exists(output_file))
        finally:
            restore_env(tmp_dir)

    def test_pdflogocreator_not_valid_image(self):
        """
        create_pdf_logo_creator test with invalid image
        """

        tmp_dir = prepare_env("pdflogocreator_not_existent_invalid")

        image_file = os.path.join("tests", "test_files", "image_invalid.png")
        output_file = os.path.join(tmp_dir, "test.pdf")

        pdf_logo = PdfLogoCreator.create_pdf_logo_creator(
            image_file,
            output_file,
            Point(50, 50),
            Point(6, 6),
        )

        # check if the file exist
        try:
            self.assertIsNone(pdf_logo)
            self.assertFalse(os.path.exists(output_file))
        finally:
            restore_env(tmp_dir)


if __name__ == "__main__":
    unittest.main()
