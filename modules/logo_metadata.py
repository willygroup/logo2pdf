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

        default_values = '{"name":"","pdf_hash":"","image":{"width":30,"height":30,"pos_x":12,"pos_y":12}}'
        # convert into JSON:
        self.data = json.loads(default_values)

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
            return False

    def set_name(self, name: str):
        """
        Set metadata name
        """

        if "name" in self.data:
            self.data["name"] = name

    def set_hash(self, hash: str):
        """
        Set metadata hash
        """
        if "pdf_hash" in self.data:
            self.data["pdf_hash"] = hash

    def set_image_size(self, width: int, height: int):
        """
        Set metadata image size
        """
        if "image" in self.data:
            if "width" in self.data["image"]:
                self.data["image"]["width"] = width
            if "height" in self.data["image"]:
                self.data["image"]["height"] = height

    def set_image_position(self, x: int, y: int):
        """
        Set metadata position
        """
        if self.data and self.data["image"]:
            if "pos_x" in self.data["image"]:
                self.data["image"]["pos_x"] = x
            if "pos_y" in self.data["image"]:
                self.data["image"]["pos_y"] = y
