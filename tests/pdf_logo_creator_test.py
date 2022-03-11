import unittest


from modules.pdf_logo_creator import PdfLogoCreator, Point


class TestPdfLogoCreatorMethods(unittest.TestCase):
    """
    Testing PdfLogoCreator
    """

    def test_init(self):
        """
        Init method test
        """

        _ = PdfLogoCreator(
            "tests/test_files/image_logo.png",
            "/tmp/test.pdf",
            Point(50, 50),
            Point(6, 6),
        )


if __name__ == "__main__":
    unittest.main()
