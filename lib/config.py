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

        self.__overrides = {}
        self.__config_file = config_file


    def configure(self):
        """
        Create JS8Call CLI configuration dictionary
        """

        config = {}

        with open(self.__config_file, "r") as f:
            config = json.loads(f.read())
        
        config.update(self.__overrides)

        return config



    def set_gpsd_connection(self, host=None, port=None, proto=None):
        """
        Set gpsd connection information.
        """

        if host is not None:
            self.__overrides['js8call_host'] = host

        if port is not None:
            self.__overrides['js8call_port'] = port


    def set_js8_connection(self, host=None, port=None, proto=None):
        """
        Set JS8Call API connection information.
        """

        if host is not None:
            self.__overrides['js8call_host'] = host

        if port is not None:
            self.__overrides['js8call_port'] = port

        if proto is not None:
            self.__overrides['js8call_proto'] = proto


    def set_maidenhead(self, level=None):
        """
        Set maidenhead coordinate accuracy.
        """

        if level is not None:
            self.__overrides['grid_level'] = level
