
"""
This file is part of js8cli by ThreeSixes https://github.com/threesixes
"""

from pprint import pprint
from pprint import pformat
import json
import socket
import traceback


class JS8CallAPI:
    """
    JS8Call API
    """
    def __init__(self, host, port, mode="tcp"):
        self.__host = host
        self.__port = port

        if mode in ["tcp", "udp"]:
            self.__mode = mode
        else:
            raise ValueError("Mode must be one of: tcp, udp")


    def __send_message(self, msg):
        """
        Send a message to JS8Call.
        """

        if self.__mode == "tcp":
            self.__send_tcp(json.dumps(msg))
        elif self.__mode == "udp":
            self.__send_udp(json.dumps(msg))


    def __send_tcp(self, msg):
        """
        Send data to host as TCP.
        """

        data = ""
        msg = msg + "\n"

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.__host, self.__port))
                s.sendall(msg.encode())
            finally:
                s.close()


    def __send_udp(self, msg):
        """
        Send data to host as UDP.
        """

        data = ""
        msg = msg + "\n"

        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.__host, self.__port)

        try:
            sent = sock.sendto(msg, server_address)
        finally:
            sock.close()


    def set_grid(self, grid):
        """
        Set the current grid square in JS8Call.
        """

        grid_msg = {
            "params": {},
            "type": "STATION.SET_GRID",
            "value": grid
        } 

        self.__send_message(grid_msg)


    def send_message(self, text):
        """
        Send a message.
        """

        set_msg = {
            "params": {},
            "type": "TX.SEND_MESSAGE",
            "value": text
        } 

        self.__send_message(set_msg)


    def set_text(self, text):
        """
        Set message text.
        """

        set_msg = {
            "params": {},
            "type": "TX.SET_TEXT",
            "value": text
        } 

        self.__send_message(set_msg)
