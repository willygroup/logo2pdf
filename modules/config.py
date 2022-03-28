import configparser

# import logging

# logger = logging.getLogger("config_mod")


class Config:
    def __init__(self, dirname, filename):
        """
        Initialize the Config class
        """
        self.dirname = dirname
        self.filename = filename

    def load_config(self):
        """
        Load the config from a file
        """
        try:
            with open(self.filename, encoding="UTF-8") as file:
                data = configparser.ConfigParser()
                data.read_file(file)
                self.config_logo_name = data["DEFAULT"]["logo_name"]
                file.close()
        except IOError:
            # logger.error("error reading config file")
            return False
        except Exception as ex:
            print("Exception: {}".format(type(ex).__name__))
            return False
        return True

    def set_config(
        self,
        logo_name: str,
    ):
        """
        Set the config values
        """
        self.config_logo_name = logo_name
        return self.write_config()

    def default(self):
        """
        Set the config default values
        """
        self.config_logo_name = "willygroup"
        return self.write_config()

    def write_config(self):
        """
        Write the config on a file
        """
        try:
            with open(self.filename, "w", encoding="UTF-8") as configfile:
                data = configparser.ConfigParser()
                data["DEFAULT"] = {"logo_name": self.config_logo_name}
                data.write(configfile)
                configfile.close()
        except IOError:
            # logger.error("error writing config file")
            return False
        return True
