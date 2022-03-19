import json
import os
from typing import Dict

# import logging

# logger = logging.getLogger("config_mod")


class LogoMetadata:
    def __init__(self, dirname, name):
        """
        Initialize the LogoMetadata class
        """
        self.file_path = os.path.join(dirname, "files", "logos", name + ".json")

    def load_metadata(self) -> bool:
        """
        Load json from file
        """
        try:
            with open(self.file_path, "r") as f:
                self.data = json.load(f)
                f.close()
                if not isinstance(self.data, Dict):
                    return False
                return True
        except Exception as e:
            print(type(e).__name__)
            return False

    def store_metadata(self) -> bool:
        """
        Store json on file
        """
        # Serializing json
        json_object = json.dumps(self.data, indent=4)

        try:
            with open(self.file_path, "w") as outfile:
                outfile.write(json_object)
                outfile.close()
                return True
        except Exception as e:
            print(type(e).__name__)
            return False

    def set_name(self, name: str):
        """
        Set metadata name
        """
        if self.data["name"]:
            self.data["name"] = name

    def set_hash(self, hash: str):
        """
        Set metadata hash
        """
        if self.data["pdf_hash"]:
            self.data["pdf_hash"] = hash

    def set_image_size(self, width: int, height: int):
        """
        Set metadata image size
        """
        if self.data["image"]:
            if self.data["image"]["width"]:
                self.data["image"]["width"] = width
            if self.data["image"]["height"]:
                self.data["image"]["height"] = width

    def set_image_position(self, x: int, y: int):
        """
        Set metadata position
        """
        if self.data["image"]:
            if self.data["image"]["pos_x"]:
                self.data["image"]["pos_x"] = x
            if self.data["image"]["pos_y"]:
                self.data["image"]["pos_y"] = y
