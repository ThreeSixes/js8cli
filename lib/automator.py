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
        self.__retry_timers = [0, 1, 1, 2, 3, 5, 8, 13]
        self.__se = sys.stderr.write
        self.__so = sys.stdout.write


    def __timer_loop(self):
        """
        Trigger calls on a timer.
        """
        run = True 
        next_js8_update = datetime.datetime.now() + datetime.timedelta(minutes=-1)
        next_loc_update = datetime.datetime.now() + datetime.timedelta(minutes=-1)
        while run:
            js8_run = False
            loc_run = False
            if datetime.datetime.now() >= next_js8_update:
                js8_run = True
            if datetime.datetime.now() >= next_loc_update:
                loc_run = True
            if js8_run:
                if self.__config['js8call_loc_refresh_min'] > 0:
                    self.__so("Updating JS8Call location.\n")
                    self.__update_js8_location()
                    next_js8_update = datetime.datetime.now() + datetime.timedelta(
                        minutes=self.__config['js8call_loc_refresh_min'])
            if loc_run:
                if self.__config['aprs_loc_update_min'] > 0:
                    self.__so("Updating APRS grid location.\n")
                    self.__send_aprs_location()
                    next_loc_update = datetime.datetime.now() + datetime.timedelta(
                        minutes=self.__config['aprs_loc_update_min'])
            time.sleep(1)


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
                        self.__se("JS8Call API connection refused @ %s:%s\n"
                            %(self.__config['js8call_host'], self.__config['js8call_port']))
                    except ConnectionResetError:
                        self.__se("JS8Call API connection reset @ %s:%s\n"
                            %(self.__config['js8call_host'], self.__config['js8call_port']))
                else:
                    self.__se("No GPS lock. Couldn't set JS8Call grid square.\n")
            except ConnectionRefusedError:
                self.__se("GPSD connection refused @ %s:%s\n"
                    %(self.__config['js8call_host'], self.__config['js8call_port']))
            except ConnectionResetError:
                self.__se("GPSD connection reset @ %s:%s\n"
                    %(self.__config['js8call_host'], self.__config['js8call_port']))
            if try_action:
                time.sleep(self.__retry_timers[step])
                if step < len(step):
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
                if mh['lock'] is True and mh['grid'] != "":
                    try:
                        js8callapi.send_message("@APRSIS GRID %s" %mh['grid'])
                        try_action = False
                    except ConnectionRefusedError:
                        self.__se("JS8Call connection refused @ %s:%s\n"
                            %(self.__config['js8call_host'], self.__config['js8call_port']))
                    except ConnectionResetError:
                        self.__se("JS8Call connection reset @ %s:%s\n"
                            %(self.__config['js8call_host'], self.__config['js8call_port']))
                else:
                    self.__se("No GPS lock. Couldn't send position to APRS.\n")
            except ConnectionRefusedError:
                self.__se("GPSD connection refused @ %s:%s\n"
                    %(self.__config['js8call_host'], self.__config['js8call_port']))
            except ConnectionResetError:
                self.__se("GPSD connection reset @ %s:%s\n"
                    %(self.__config['js8call_host'], self.__config['js8call_port']))
            if try_action:
                time.sleep(self.__retry_timers[step])
                step += 1


    def run(self):
        """
        Automatically
        """
        self.__so("Daemon running.\n")
        try:
            self.__timer_loop()
        except (KeyboardInterrupt, SystemExit):
            self.__so("Caught interrupt.\n")
        self.__so("Daemon exiting.\n")
