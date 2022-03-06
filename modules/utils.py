"""
Utilities module
"""

import sys
import os

from modules.pdf_creator import PdfCreator


def create_environment(dirname):
    """
    Prepare the execution environment
    """

    logo_file = os.path.join(dirname, "files", "logo.pdf")
    if not os.path.exists("files"):
        os.makedirs("files")
    if not os.path.exists(os.path.join(dirname, "files", "nologo")):
        os.makedirs(os.path.join(dirname, "files", "nologo"))
    if not os.path.exists(os.path.join(dirname, "files", "logo")):
        os.makedirs(os.path.join(dirname, "files", "logo"))
    if not logo_file:
        print("No files/logo.pdf file found!")
        sys.exit(1)
    print("Check on logo: " + logo_file)
    if not PdfCreator.checks_valid_pdf(logo_file):
        print("logo.pdf is not a valid pdf file!")
        sys.exit(1)
