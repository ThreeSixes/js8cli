"""
This file is part of js8cli by ThreeSixes https://github.com/threesixes
"""

import datetime
import sys
import time

from .location import Location
from .js8call_api import JS8CallAPI


class Automator:
    def __init__(self, config):
        """
        Automate JS8Call actions
        """
        self.__config = config
        self.__retry_timers = [0, 1, 1, 2, 3, 5, 8]
        self.__se = sys.stderr.write
        self.__so = sys.stdout.write


    def __timer_loop(self):
        """
        Time calls.
        """
        run = True 
        last_js8_update = None
        last_loc_update = None
        while run:
            if self.__config['js8call_loc_refresh_min'] > 0:
                    self.__update_js8_location()
            if self.__config['aprs_loc_update_min'] > 0:
                self.__send_aprs_location()
            time.sleep(1)
            run = False # TOOD unhack.


    def __update_js8_location(self):
        """
        Update JS8Call's location.
        """
        try_action = True
        step = 0
        while try_action:
            js8callapi = JS8CallAPI(self.__config['js8call_host'], self.__config['js8call_port'])
            try:
                location = Location(gpsd_host=self.__config['gpsd_host'], gpsd_port=self.__config['gpsd_port'])
                mh = location.maidenhead(level=self.__config['grid_level'])
                if mh['lock']:
                    try:
                        js8callapi.set_grid(mh['grid'])
                        try_action = False
                    except ConnectionRefusedError:
                        se("JS8Call API connection refused @ %s:%s\n"
                            %(self.__config['js8call_host'], self.__config['js8call_port']))
                    except ConnectionResetError:
                        se("JS8Call API connection reset @ %s:%s\n"
                            %(self.__config['js8call_host'], self.__config['js8call_port']))
                else:
                    se("No GPS lock. Couldn't set JS8Call grid square.\n")
            except ConnectionRefusedError:
                se("GPSD connection refused @ %s:%s\n"
                    %(self.__config['js8call_host'], self.__config['js8call_port']))
            except ConnectionResetError:
                se("GPSD connection reset @ %s:%s\n"
                    %(self.__config['js8call_host'], self.__config['js8call_port']))
            if try_action:
                time.sleep(self.__retry_timers[step])
                step += 1


    def __send_aprs_location(self):
        """
        Send an APRS location update.
        """
        try_action = True
        step = 0
        while try_action:
            js8callapi = JS8CallAPI(self.__config['js8call_host'], self.__config['js8call_port'])
            try:
                location = Location(gpsd_host=self.__config['gpsd_host'], gpsd_port=self.__config['gpsd_port'])
                mh = location.maidenhead(level=self.__config['grid_level'])
                if mh['lock']:
                    try:
                        js8callapi.send_message("@APRSIS GRID %s" %mh['grid'])
                        try_action = False
                    except ConnectionRefusedError:
                        se("JS8Call connection refused @ %s:%s\n"
                            %(self.__config['js8call_host'], self.__config['js8call_port']))
                    except ConnectionResetError:
                        se("JS8Call connection reset @ %s:%s\n"
                            %(self.__config['js8call_host'], self.__config['js8call_port']))
                else:
                    se("No GPS lock. Couldn't send position to APRS.\n")
            except ConnectionRefusedError:
                se("GPSD connection refused @ %s:%s\n"
                    %(self.__config['js8call_host'], self.__config['js8call_port']))
            except ConnectionResetError:
                se("GPSD connection reset @ %s:%s\n"
                    %(self.__config['js8call_host'], self.__config['js8call_port']))
            if try_action:
                time.sleep(self.__retry_timers[step])
                step += 1


    def run(self):
        """
        Automatically
        """
        self.__so("Daemon running.\n")
        self.__timer_loop()
        self.__so("Daemon exiting.\n")
