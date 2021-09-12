import os
import unittest

from modules.pdf_creator import PdfCreator


dirname = os.path.realpath(__file__).replace("pdf_creator_test.py", "")


class TestPdfCreatorMethods(unittest.TestCase):
    def test_1(self):
        res = False
        self.assertFalse(res)

    def test_2(self):
        res = False
        self.assertFalse(not res)


if __name__ == "__main__":
    unittest.main()
