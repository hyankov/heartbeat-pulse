# Import system
from os import path
import configparser


class Config:
    @staticmethod
    def load(section_name, key_name):
        _filename = "config/app.config.ini"

        if not section_name:
            raise ValueError("section_name is required")

        if not key_name:
            raise ValueError("key_name is required")

        if not path.exists(_filename):
            raise ValueError("Config file '{}' not found!".format(_filename))

        config = configparser.RawConfigParser()
        config.read(_filename)

        if not config[section_name]:
            raise ValueError("Config section '{}' is missing!".format(section_name))

        return config[section_name].get(key_name)
