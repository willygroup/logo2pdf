import os
import unittest
import json

from modules.logo_metadata import LogoMetadata

from modules.paths import Paths
from tests.commons import (
    create_directory,
    create_metadata_file,
    prepare_env,
    restore_env,
)


class TestLogoMetadataMethods(unittest.TestCase):
    """
    Testing LogoMetadata
    """

    def test_init(self):
        """
        Init method test
        """
        logo_name = "xxx"

        tmp_dir = prepare_env("logo_metadata_init")
        Paths.init(tmp_dir)
        try:
            logo_metadata = LogoMetadata(logo_name)

            self.assertEqual(
                logo_metadata.file_path,
                os.path.join(tmp_dir, "files", "logos", logo_name + ".json"),
            )
        except Exception as e:
            print(e)
            self.fail()
        finally:
            restore_env(tmp_dir)

    def test_load_metadata_not_existant(self):
        """
        LoadMetadata fail test
        """
        logo_name = "xxx"

        tmp_dir = prepare_env("logo_metadata_load")
        try:
            logo_metadata = LogoMetadata(logo_name)
            res = logo_metadata.load_metadata()

            self.assertFalse(res)
        except Exception as e:
            print(e)
            self.fail()
        finally:
            restore_env(tmp_dir)

    def test_load_metadata_invalid_json(self):
        """
        LoadMetadata invalid json
        """
        tmp_dir = prepare_env("logo_metadata_load")

        logo_name = "xxx"
        create_directory(os.path.join(tmp_dir, "files"))
        create_directory(os.path.join(tmp_dir, "files", "logos"))
        create_metadata_file(
            os.path.join(tmp_dir, "files", "logos", logo_name + ".json"), False
        )

        try:
            logo_metadata = LogoMetadata(logo_name)
            res = logo_metadata.load_metadata()

            self.assertFalse(res)
        except Exception as e:
            print(e)
            self.fail()
        finally:
            restore_env(tmp_dir)

    def test_load_metadata_valid_json(self):
        """
        LoadMetadata valid json
        """
        tmp_dir = prepare_env("logo_metadata_load")
        Paths.init(tmp_dir)

        logo_name = "xxx"
        create_directory(Paths.files)
        create_directory(Paths.logos)
        create_metadata_file(Paths.logo(logo_name + ".json"), True)

        try:
            logo_metadata = LogoMetadata(logo_name)
            res = logo_metadata.load_metadata()

            self.assertTrue(res)
            self.assertTrue(type(logo_metadata.data), type({}))
            self.assertEqual(logo_metadata.data["name"], "hello")
        except Exception as e:
            print(e)
            self.fail()
        finally:
            restore_env(tmp_dir)

    def test_store_metadata(self):
        """
        StoreMetadata
        """
        tmp_dir = prepare_env("logo_metadata_load")
        Paths.init(tmp_dir)
        logo_name = "store"
        create_directory(Paths.files)
        create_directory(Paths.logos)
        create_metadata_file(Paths.logo(logo_name + ".json"), True)

        try:
            logo_metadata = LogoMetadata(logo_name)
            res = logo_metadata.load_metadata()

            self.assertTrue(res)
            logo_metadata.data["name"] = "goodbye"
            res = logo_metadata.store_metadata()

            with open(Paths.logo(logo_name + ".json"), "r") as json_file:
                json_struct = json.load(json_file)
                self.assertTrue(json_struct["name"], "goodbye")
                json_file.close()
        except Exception as e:
            print(e)
            self.fail()
        finally:
            restore_env(tmp_dir)

    def test_store_setters(self):
        """
        Metadata setters
        """
        tmp_dir = prepare_env("logo_metadata_load")
        Paths.init(tmp_dir)
        logo_name = "store"
        create_directory(Paths.files)
        create_directory(Paths.logos)
        create_metadata_file(Paths.logo(logo_name + ".json"), True)

        try:
            logo_metadata = LogoMetadata(logo_name)
            res = logo_metadata.load_metadata()

            self.assertTrue(res)

            logo_metadata.set_name("new_name")
            logo_metadata.set_hash("new_hash")
            logo_metadata.set_image_size(False, 250, 150)
            logo_metadata.set_image_position(25, 15)

            res = logo_metadata.store_metadata()

            with open(Paths.logo(logo_name + ".json"), "r") as json_file:
                json_struct = json.load(json_file)
                self.assertTrue(json_struct["name"], "new_name")
                self.assertTrue(json_struct["pdf_hash"], "new_hash")
                self.assertTrue(json_struct["image"]["width"], 250)
                self.assertTrue(json_struct["image"]["height"], 150)
                self.assertTrue(json_struct["image"]["pos_x"], 25)
                self.assertTrue(json_struct["image"]["pos_y"], 15)
                json_file.close()
        except Exception as e:
            print(e)
            self.fail()
        finally:
            restore_env(tmp_dir)


if __name__ == "__main__":
    unittest.main()
