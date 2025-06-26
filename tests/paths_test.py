import os
import unittest


from tests.common import (
    create_config_file,
    create_directory,
    prepare_env,
    restore_env,
)
from modules.paths import Paths


class TestPathsMethods(unittest.TestCase):
    """
    Testing Paths
    """

    def test_init(self):
        """
        Init method test
        """

        tmp_dir = prepare_env("paths_init")

        try:
            paths = Paths.init(tmp_dir)

            self.assertEqual(Paths.base, tmp_dir)

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_image(self):
        """
        image method test
        """

        tmp_dir = prepare_env("paths_image")

        try:
            Paths.init(tmp_dir)
            self.assertEqual(Paths.image("image.png"),
                             os.path.join(tmp_dir, "files", "images", "image.png"))

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_locale(self):
        """
        locale method test
        """

        tmp_dir = prepare_env("paths_locale")

        try:
            Paths.init(tmp_dir)
            self.assertEqual(Paths.locale("file"),
                             os.path.join(tmp_dir, "files", "locale", "file"))

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_file(self):
        """
        file method test
        """

        tmp_dir = prepare_env("paths_file")

        try:
            Paths.init(tmp_dir)
            self.assertEqual(Paths.file("file"),
                             os.path.join(tmp_dir, "files", "file"))

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_logo(self):
        """
        logo method test
        """

        tmp_dir = prepare_env("paths_logo")

        try:
            Paths.init(tmp_dir)
            self.assertEqual(Paths.logo("logo.png"),
                             os.path.join(tmp_dir, "files", "logos", "logo.png"))

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_out(self):
        """
        out method test
        """

        tmp_dir = prepare_env("paths_out")

        try:
            Paths.init(tmp_dir)
            self.assertEqual(Paths.out("file"),
                             os.path.join(tmp_dir, "output", "file"))

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)


if __name__ == "__main__":
    unittest.main()
