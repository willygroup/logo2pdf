import os
import unittest

from modules.paths import Paths
from tests.commons import (
    prepare_env,
    restore_env,
)


class TestPathsMethods(unittest.TestCase):
    """
    Testing Paths
    """

    def test_init(self) -> None:
        """
        Init method test
        """

        tmp_dir = prepare_env("paths_init")

        try:
            Paths.init(tmp_dir)

            self.assertEqual(Paths.base, tmp_dir)

        except (Exception,) as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_image(self) -> None:
        """
        image method test
        """

        tmp_dir = prepare_env("paths_image")

        try:
            Paths.init(tmp_dir)
            self.assertEqual(
                Paths.image("image.png"),
                os.path.join(tmp_dir, "files", "images", "image.png"),
            )

        except (Exception,) as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_locale(self) -> None:
        """
        locale method test
        """

        tmp_dir = prepare_env("paths_locale")

        try:
            Paths.init(tmp_dir)
            self.assertEqual(
                Paths.locale("file"), os.path.join(tmp_dir, "files", "locale", "file")
            )

        except (Exception,) as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_file(self) -> None:
        """
        file method test
        """

        tmp_dir = prepare_env("paths_file")

        try:
            Paths.init(tmp_dir)
            self.assertEqual(Paths.file("file"), os.path.join(tmp_dir, "files", "file"))

        except (Exception,) as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)
