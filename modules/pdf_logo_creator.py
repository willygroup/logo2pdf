"""
Create a pdf with a logo from scratch
"""
from fpdf import FPDF  # fpdf class


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PdfLogoCreator:
    def __init__(
        self, logo_file, output_file, dimension: Point, position: Point = Point(5, 5)
    ) -> None:

        self.logo_file = logo_file
        self.output_file = output_file
        self.logo_dimension = dimension
        self.logo_position = position
        self.create_pdf_logo()

    @classmethod
    def create_pdf_logo_creator(
        cls, logo_file, output_file, dimension: Point, position: Point = Point(5, 5)
    ):
        try:
            res = cls(logo_file, output_file, dimension, position)
        except (FileNotFoundError, RuntimeError):
            return None
        return res

    def create_pdf_logo(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")  # default
        pdf.add_page()
        pdf.set_xy(self.logo_position.x, self.logo_position.y)
        pdf.image(
            self.logo_file,
            link="",
            type="",
            w=self.logo_dimension.x,
            h=self.logo_dimension.y,
        )
        pdf.output(self.output_file, "F")
