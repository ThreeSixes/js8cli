"""
This file is part of js8cli by ThreeSixes https://github.com/threesixes
"""

from pprint import pprint
import json
import os
import sys

class Configurator:
    """
    Generate the JS8Call CLI configuration
    """
    def __init__(self, config_file):

        self.__overrides = {}
        self.__config_file = config_file
        self.__log_levels = {
            "default": 0,
            "debug": 10,
            "info": 20,
            "warn": 30,
            "error": 40,
            "critical": 50
        }


    def configure(self):
        """
        Create JS8Call CLI configuration dictionary
        """

        config = {}

        with open(self.__config_file, "r") as f:
            config = json.loads(f.read())

        config.update(self.__overrides)

        if 'daemon_log_level' in config:
            if config['daemon_log_level'] in self.__log_levels:
                config['daemon_log_level'] = self.__log_levels[config['daemon_log_level']]
            else:
                sys.stderr.write("daemon_log_level should be set to one of: %s.\n"
                    %self.__log_levels.keys())
        else:
            config['daemon_log_level'] = self.__log_levels['default']

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
