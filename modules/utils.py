"""
Utilities module
"""

import platform
import sys
import os
import subprocess

from modules.paths import Paths
from modules.pdf_creator import PdfCreator


def create_environment():
    """
    Prepare the execution environment
    """

    logo_file = Paths.logo("logo.pdf")
    if not os.path.exists("files"):
        os.makedirs("files")
    if not os.path.exists(Paths.out("nologo")):
        os.makedirs(Paths.out("nologo"))
    if not os.path.exists(Paths.out("logo")):
        os.makedirs(Paths.out("logo"))
    if not logo_file:
        print("No files/logo.pdf file found!")
        sys.exit(1)
    if not PdfCreator.checks_valid_pdf(logo_file):
        print("logo.pdf is not a valid pdf file!")
        sys.exit(1)


def open_directory(directory):
    """
    Open the output directory
    """
    os_name = platform.system()
    if os_name == "Linux":
        subprocess.Popen(["xdg-open", directory])
    elif os_name == "Windows":
        # pylint: disable=no-member
        os.startfile(directory)
    elif os_name == "Darwin":
        subprocess.Popen(["open", directory])
    else:
        # logger.error("Error: Operating System not recognized!")
        return False
    return True
