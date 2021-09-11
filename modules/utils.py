"""
Utilities module
"""

import sys
import os
import filetype

# // TODO replace with a proper logging system
def log(msg):
    """
    Logging facility
    """
    debug_trace = True
    if debug_trace:
        print(">>" + msg)


def create_environment(dirname):
    """
    Prepare the execution environment
    """

    if not os.path.exists("files"):
        os.makedirs("files")
    if not os.path.exists("files/nologo"):
        os.makedirs("files/nologo")
    if not os.path.exists("files/logo"):
        os.makedirs("files/logo")
    if not os.path.exists("files/logo.pdf"):
        log("No files/logo.pdf file found!")
        sys.exit(1)
    kind = filetype.guess(os.path.join(dirname, "files", "logo.pdf"))
    if kind is None or kind.mime != "application/pdf":
        log("logo.pdf is not a valid pdf file! mimetype: " + kind.mime)
        sys.exit(1)
