"""
Contains various utility functions and classes used by the groundstation
module.
"""

import os
import time


def discover_serial_port():
    """
    Returns a ``str`` containing the absolute filepath to the discovered
    serial port.

    Returns ``False`` if no serial connection could be found
    """
    for i in range(10):
        path = "/dev/ttyACM{}".format(str(i))
        if os.path.exists(path):
            return path

    raise OSError("Unable to find serial port.")


def convert_time(time_ms):
    """
    Converts a time in milliseconds to a time in seconds.
    """
    return time_ms / 1000


def average(iterable):
    """
    Returns the average of a list of numbers.
    """
    return sum(iterable) / len(iterable)


def listener_get_log_file():
    """
    Returns a filename for a CanSat log file.
    """
    return "cansat_{}.log".format(str(int(time.time())))


class Buffer(object):
    """
    Acts as a buffer on a ``FileObject``.

    ``get_line`` can be used to get full lines of data.
    """
    def __init__(self, handle):
        self.handle = handle
        self.line_buf = ""

    def get_data(self, amount):
        buf = ""

        while len(buf) != amount:
            buf += self.handle.read(1)

        return buf

    def read(self, amount):
        return self.get_data(amount)

    def get_line(self):
        """
        Returns a string with a line of data.
        Returns ``None`` if insufficient data available.
        """
        self.line_buf += self.handle.readline()

        if "\n" in self.line_buf:
            result = self.line_buf
            self.line_buf = ""
            return result
        else:
            return

    def readline(self):
        return self.handle.readline()
