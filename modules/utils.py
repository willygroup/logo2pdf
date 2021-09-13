"""
Utilities module
"""

from modules.pdf_creator import PdfCreator
import sys
import os
import magic


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
    if checks_valid_pdf(logo_file) != True:
        print("logo.pdf is not a valid pdf file!")
        sys.exit(1)
