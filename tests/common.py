import os
import shutil

dirname = os.path.realpath(__file__).replace("common.py", "")


def create_file(filename):
    with open(filename, "w") as f:
        f.write("file: " + filename)


def create_pdf_file(filename):
    shutil.copyfile(os.path.join(dirname, "test_files", "nologo_file.pdf"), filename)


def create_directory(pathname):
    os.makedirs(pathname, exist_ok=True)


def set_environment(dirname):
    reset_environment(dirname)
    create_directory(os.path.join(dirname, "tmp"))


def reset_environment(dirname):
    shutil.rmtree(os.path.join(dirname, "tmp"), ignore_errors=True)
