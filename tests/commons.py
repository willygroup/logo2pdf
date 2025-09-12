import os
import shutil
import tempfile

from modules.paths import Paths

test_directory = os.path.realpath(__file__).replace(os.path.basename(__file__), "")


def create_file(filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("file: " + filename)


def create_pdf_file(dest_filename, valid=True):
    if valid:
        shutil.copyfile(
            os.path.join(test_directory, "test_files", "nologo_file.pdf"), dest_filename
        )
    else:
        shutil.copyfile(
            os.path.join(test_directory, "test_files", "invalid.pdf"), dest_filename
        )


def create_config_file(dest_filename, valid=True):
    if valid:
        shutil.copyfile(
            os.path.join(test_directory, "test_files", "config.conf"), dest_filename
        )
    else:
        shutil.copyfile(
            os.path.join(test_directory, "test_files", "bad_config.conf"), dest_filename
        )


def create_metadata_file(dest_filename, valid=True):
    if valid:
        shutil.copyfile(
            os.path.join(test_directory, "test_files", "valid_metadata.json"),
            dest_filename,
        )
    else:
        shutil.copyfile(
            os.path.join(test_directory, "test_files", "invalid_metadata.json"),
            dest_filename,
        )


def create_logo_file(dest_filename):
    shutil.copyfile(
        os.path.join(test_directory, "test_files", "logo.pdf"), dest_filename
    )


def create_directory(pathname):
    os.makedirs(pathname, exist_ok=True)


def prepare_env(suffix) -> str:
    tmp_dir = tempfile.mkdtemp(suffix, "tmp_")
    Paths.init(tmp_dir)
    return tmp_dir


def restore_env(directory):
    shutil.rmtree(directory, ignore_errors=True)
