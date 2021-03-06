# Import system
from os import path
import configparser


class Config:
    """
    Loads configurations.
    """

    @staticmethod
    def load(section_name, key_name):
        """
        Description
        --
        Loads a setting by setting section name and key.

        Parameters
        --
        - section_name - the name of the setting section.
        - key_name - the name of the setting key.
        """

        _filename = "config/app.ini"

        if not section_name:
            raise ValueError("section_name is required")

        if not key_name:
            raise ValueError("key_name is required")

        if not path.exists(_filename):
            raise ValueError("Config file '%s' not found!", _filename)

        config = configparser.RawConfigParser()
        config.read(_filename)

        if not config[section_name]:
            raise ValueError("Config section '%s' is missing!", section_name)

        return config[section_name].get(key_name)
