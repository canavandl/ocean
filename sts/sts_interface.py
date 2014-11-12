#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Socket API for interacting with STS series spectrometers from Ocean Optics
==============================================================================

The following hexadecimal commands and helper function are used to send
commands and queries over TCP sockets to a daemon service running on a
Raspberry Pi. The daemon services forwards the messages to the spectrometer
running the Seabreeze library and returns responses.

The SocketClient class is a thin-wrapper around the low-level python "socket"
library to assist in sending and receiving messages from the daemon service

See Also:
--------
STS Developer's Kit Programming Guide
http://oceanoptics.com/wp-content/uploads/STS-Dev-Kit-API-Manual.pdf

Seabreeze Driver Documentation
http://oceanoptics.com/product/seabreeze/
"""

import socket

__author__ = 'Luke Canavan'
__copyright__ = ''
__license__ = ''
__maintainer__ = ''
__email__ = 'canavandl@gmail.com'
__status__ = 'alpha'

DAEMON_CONSTANTS = {
  "hostname": "127.0.0.1",
  "port": 1865}

DAEMON_COMMANDS = {
  "get_version": "\x0D",
}

SPECTROMETER_STATUS = {
  "get_integration_time_minimum": "\x14",
  "get_integration_time_maximum": "\x15",
  "get_intensity_maximum": "\x16",
  "get_wavelengths": "\x0A",
  "get_serial_number": "\x0B",
  "get_name": "\x0C",
}

OCEAN_COMMANDS = {
  "set_integration_time": "\x01",
  "get_integration_time": "\x02",
  "set_boxcar_width": "\x03",
  "get_boxcar_width": "\x04",
  "set_scans_to_average": "\x05",
  "get_scans_to_average": "\x06",
  "set_target_url": "\x07",
  "get_target_url": "\x08",
  "get_spectrum": "\x09",
  "get_calibration_coefficients_from_buffer": "\x0E",
  "set_calibration_coefficients_to_buffer": "\x0F",
  "get_calibration_coefficients_from_eeprom": "\x10",
  "set_calibration_coefficients_to_eeprom": "\x11",
  "get_pixel_binning_factor": "\x12",
  "set_pixel_binning_factor": "\x13",
  "get_electric_dark_correction": "\x17",
  "set_electric_dark_correction": "\x18",
}

OCEANHANDLER_COMMANDS = {
  "get_current_status": "\x20",
  "get_current_spectrum": "\x21",
  "set_max_acquisitions": "\x22",
  "get_max_acquisitions": "\x23",
  "set_file_save_mode": "\x24",
  "get_file_save_mode": "\x25",
  "set_file_prefix": "\x26",
  "get_file_prefix": "\x27",
  "set_sequence_type": "\x28",
  "get_sequence_type": "\x29",
  "set_sequence_interval": "\x2A",
  "get_sequence_interval": "\x2B",
  "set_save_directory": "\x2C",
  "get_save_directory": "\x2D",
  "save_spectrum": "\x2E",
  "start_sequence": "\x2F",
  "pause_sequence": "\x30",
  "resume_sequence": "\x31",
  "stop_sequence": "\x32",
  "get_sequence_state": "\x33",
  "get_current_sequence_number": "\x34",
  "set_scope_mode": "\x35",
  "get_scope_mode": "\x36",
  "set_scope_interval": "\x37",
  "get_scope_interval": "\x38"}

STS_INTERFACE = DAEMON_COMMANDS
STS_INTERFACE.update(SPECTROMETER_STATUS)
STS_INTERFACE.update(OCEAN_COMMANDS)
STS_INTERFACE.update(OCEANHANDLER_COMMANDS)

### Convenience constant for null/no parameters to a command
NO_PARAMETERS = "\x00\x00"


class SocketClient(object):
    """
    Thin wrapper around low-level python 'socket' library

    Parameters
    ----------
    hostname : numeric, required
    port : numeric, required
    open_connection : bool, optional (default is True)

    Attributes
    ----------
    hostname
    port
    sock (socket object)

    Methods
    -------
    __repr__
    open_connection
    close_connection
    send_message
    receive_stream
    receive_message
    """

    def __init__(self, hostname, port, timeout=1, open_connection=True):
        self.hostname = hostname
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        if open_connection:
            self.open_connection()

    def __repr__(self):
        """
        Returns a formatted string representation.

        Returns
        -------
        unicode formatted string representation.
        """
        return 'SocketClient(hostname={0}, post={1})'.format(self.hostname,
                                                             self.port)

    def open_connection(self):
        """
        Connects to socket at self.hostname: self.port

        Returns
        -------
        None
        """
        self.sock.connect((self.hostname, self.port))

    def close_connection(self):
        """
        Disconnects from socket

        Returns
        -------
        None
        """
        self.sock.close()

    def send_message(self, message):
        """
        Sends message to service at self.hostname: self.port

        Parameters
        ----------
        message : string

        Returns
        -------
        None
        """
        self.sock.sendall(message)

    def receive_stream(self, read_length=64):
        """
        Generator function to read buffer of unknown length at
        self.hostname: self.port

        Parameters
        ----------
        length : optional

        Returns
        -------
        iterable
        """
        try:
            data = self.sock.recv(read_length)
        except socket.timeout:
            raise StopIteration

        while data:
            yield data
            data = self.sock.recv(read_length)

    def receive_message(self):
        """
        Read entire buffer from socket at self.hostname: self.port

        Returns
        -------
        string
        """
        return ''.join(list(self.receive_stream()))


def create_sts_command(command, parameter=None):
    """
    Helper function to create properly formatted commands to interact
    with STS daemon

    Sent commands are of the format:
      /STS command : hexadecimal
      /parameter byte length high : hexadecimal
      /parameter byte length low : hexadecimal
      /parameter as string : string

    Parameters
    ----------
    command : string
        hexadecimal string pertaining to command
    parameter : string or int, optional (default is None)
        for 'set' commands, the associated parameter

    Returns
    -------
    string : formatted STS command
    """
    if parameter is None:
        command += NO_PARAMETERS
    else:
        parameter = str(parameter)
        hi_bit = chr((len(parameter) & 0xFF00) >> 8)
        lo_bit = chr(len(parameter) & 0xFF)
        command += hi_bit + lo_bit + parameter
    return command

