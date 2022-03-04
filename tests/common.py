import os
import shutil
import tempfile

dirname = os.path.realpath(__file__).replace("common.py", "")


def create_file(filename):
    with open(filename, "w") as f:
        f.write("file: " + filename)


def create_pdf_file(dest_filename, valid=True):
    if valid:
        shutil.copyfile(
            os.path.join(dirname, "test_files", "nologo_file.pdf"), dest_filename
        )
    else:
        shutil.copyfile(
            os.path.join(dirname, "test_files", "invalid.pdf"), dest_filename
        )


def create_logo_file(dest_filename):
    shutil.copyfile(os.path.join(dirname, "test_files", "logo.pdf"), dest_filename)


def create_directory(pathname):
    os.makedirs(pathname, exist_ok=True)


def prepare_env(suffix):
    return tempfile.mkdtemp(suffix, "tmp_")


def restore_env(directory):
    shutil.rmtree(directory, ignore_errors=True)
