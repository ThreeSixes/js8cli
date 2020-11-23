"""
GPS and location functionality for JS8Call
"""

from pprint import pprint

import maidenhead as mh
import gpsd


class Location:
        """
        Location data class.
        """

    def __init__(self, gpsd_host='127.0.0.1', gpsd_port=2947):
        self.__gpsd_host = gpsd_host
        self.__gpsd_port = gpsd_port


    def __get_gps_location(self):
        """
        Get a GPS location from GPSD.
        """

        pos = {'alt_ft': None, 'error': False, 'lat': None, 'lon': None, 'lock': False}

        gpsd.connect(host=self.__gpsd_host, port=self.__gpsd_port)

        try:
            packet = gpsd.get_current()
            if packet.mode >= 2:
                pos['lock'] = True
                pos['lat'] = packet.lat
                pos['lon'] = packet.lon
            if packet.mode >= 3:
                pos['alt_ft'] = packet.alt
        except UserWarning:
            pos['error'] = True
            pos['lock'] = False

        return pos


    def __get_maidenhead(self, level):
        """
        Get maidenhead coordinates given an accuracy level.
        """
        
        mh_resp = {'grid': None, 'lock': False}
        loc = self.__get_gps_location()

        if loc['lock']:
            mh_resp['lock'] = True
            mh_resp['grid'] = mh.to_maiden(loc['lat'], loc['lon'], precision=level)

        return mh_resp


    def coords(self):
        """
        Get coordinates from the GPS unit.
        """

        return self.__get_gps_location()


    def maidenhead(self, level=4):
        """
        Get maidenhead grid locator from GPS.
        """

        return self.__get_maidenhead(level)