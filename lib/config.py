"""
JS8Call CLI configurator
"""

from pprint import pprint
import json
import os

class Configurator:
    def __init__(self, config_file):
        """
        Generate the JS8Call CLI configuration
        """

        self.__config_file = config_file


    def configure(self):
        """
        Create JS8Call CLI configuration dictionary
        """

        config = {}

        with open(self.__config_file, "r") as f:
            config = json.loads(f.read())

        return config
