"""
JS8Call CLI configurator
"""

from pprint import pprint
import json
import os

class Configurator:
    """
    Generate the JS8Call CLI configuration
    """
    def __init__(self, config_file):

        self.__config_file = config_file


    def configure(self):
        """
        Create JS8Call CLI configuration dictionary
        """

        config = {}

        with open(self.__config_file, "r") as f:
            config = json.loads(f.read())

        return config
