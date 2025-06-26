import os
import unittest


from tests.common import (
    create_config_file,
    prepare_env,
    restore_env,
)
from modules.config import Config


class TestConfigMethods(unittest.TestCase):
    """
    Testing Config
    """

    def test_init(self):
        """
        Init method test
        """

        tmp_dir = prepare_env("config_init")
        config_file = os.path.join(tmp_dir, "config.conf")

        create_config_file(config_file)

        try:
            config = Config(config_file)

            self.assertEqual(config.filename, config_file)

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_load_data(self):
        """
        LoadData method test
        """

        tmp_dir = prepare_env("config_load_data")

        config_file = os.path.join(tmp_dir, "config.conf")

        create_config_file(config_file)

        try:
            config = Config(config_file)

            res = config.load_config()

            self.assertTrue(res)
            self.assertEqual(config.config_logo_name, "willygroup")

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_load_not_existent_file(self):
        """
        LoadData method test with bad config file
        """

        tmp_dir = prepare_env("config_load_bad_data")

        config_file = os.path.join(tmp_dir, "config.conf")

        try:
            config = Config(config_file)

            res = config.load_config()

            self.assertFalse(res)

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_load_bad_data(self):
        """
        LoadData method test with bad config file
        """

        tmp_dir = prepare_env("config_load_bad_data")

        config_file = os.path.join(tmp_dir, "config.conf")

        create_config_file(config_file, False)

        try:
            config = Config(config_file)

            res = config.load_config()

            self.assertFalse(res)

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_set_config(self):
        """
        SetConfig method test with bad config file
        """
        tmp_dir = prepare_env("config_set_config")

        config_file = os.path.join(tmp_dir, "anyfile.conf")

        try:

            config = Config(config_file)

            res = config.set_config("new_logo")

            self.assertTrue(res)
            self.assertEqual(config.config_logo_name, "new_logo")

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)

    def test_write_config(self):
        """
        WriteConfig method test with bad config file
        """

        tmp_dir = prepare_env("config_write_config")

        config_file = os.path.join(tmp_dir, "config.conf")

        try:
            config = Config(config_file)

            res = config.config_logo_name = "new_logo"

            self.assertTrue(res)
            self.assertFalse(os.path.isfile(config_file))

            res = config.write_config()

            self.assertTrue(res)

            self.assertTrue(os.path.isfile(config_file))

        except Exception as e:
            print(e)
            self.fail()

        finally:
            restore_env(tmp_dir)


if __name__ == "__main__":
    unittest.main()
