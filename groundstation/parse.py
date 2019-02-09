"""
Contains functions and classes used to parse, handle, validate and interpret
data received from the CanSat (or Faker).
"""

from .exceptions import (ParseError, MalformedPacket, InvalidLine,
                         CRCValidationError)
from .calculate import (calculate_temp_NTC, calculate_press, calculate_height,
                        calculate_gyr, calculate_acc, calculate_mag,
                        verify_crc, _calculate_crc)
from .utilities import convert_time
from .config import EXAMPLE_DATA_CONFIG

from copy import copy

import struct
from io import BytesIO

import re

HEAD = "SGCan"
MAGIC = 0xFF
HEAD_SEP = ">"  # Separates Head of datastring.
DATA_SEP = "|"  # Separates data-points of datastring.
FIELD_SEP = ":"  # Separates key and value in a data field.
REQUIRED_FIELDS = ["Time", "Press", "NTC", "GyrX", "GyrY", "GyrZ",
                   "AccX", "AccY", "AccZ", "MagX", "MagY", "MagZ", "Lat",
                   "Sat"]

VALID_PATTERN = re.compile(r"SGCanScience>(\w+:[-.0-9]+\|?)+")


def validate_line(line):
    """
    Validates ``line``.
    """
    # if not VALID_PATTERN.match(line):
    #     raise MalformedPacket("Got malformed packet: {}".format(line))
    return True


def handle_key(key):
    """
    Handles ``key``.
    """
    return key


def handle_value(value):
    """
    Handles ``value`` by stripping new lines and converting to a float value.
    """
    value = value.replace("\n", "")
    value = float(value)

    return value


def read_ubyte(buf):
    """
    Reads an integer from `buf`.
    """
    return ord(buf.read(1))


def read_int(buf):
    """
    Reads an integer from `buf`.
    """
    return struct.unpack("h", buf.read(2))[0]


def read_uint(buf, endianness=""):
    """
    Reads an unsigned integer from `buf`.
    """
    return struct.unpack(endianness + "H", buf.read(2))[0]


def read_unsigned_long(buf):
    """
    Reads an unsigned long from `buf`.
    """
    return struct.unpack("I", buf.read(4))[0]


def read_signed_long(buf):
    """
    Reads an unsigned long from `buf`.
    """
    return struct.unpack("i", buf.read(4))[0]


def read_double(buf):
    """
    Reads a double from `buf`.
    """
    return struct.unpack("f", buf.read(4))[0]


def unskew_buf(buf):
    """
    Returns the `buf` to a working state.
    """
    sbuf = bytes()

    while True:
        pass


def parse_line(buf, data_config=None):
    """Parses a line of output from the CanSat."""
    if data_config is None:
        data_config = copy(EXAMPLE_DATA_CONFIG)

    result = {}

    head = buf.read(len(HEAD))
    if head != HEAD:
        buf.readline()  # Try to reset state to next new line.
        raise MalformedPacket("Wrong HEAD.")

    version = buf.read(1)

    packet_size = read_ubyte(buf)

    packet = buf.read(packet_size)

    data_buf = BytesIO(bytes([ord(x) for x in packet]))

    rest = buf.readline()

    try:
        assert(ord(rest[0]) == MAGIC)
        assert(rest[1] == "\n")
        assert(len(rest) == 2)
    except AssertionError:
        raise MalformedPacket("Invalid tail.")

    result["GyrX"] = calculate_gyr(read_int(data_buf))
    result["GyrY"] = calculate_gyr(read_int(data_buf))
    result["GyrZ"] = calculate_gyr(read_int(data_buf))

    result["AccX"] = calculate_acc(read_int(data_buf), "x")
    result["AccY"] = calculate_acc(read_int(data_buf), "y")
    result["AccZ"] = calculate_acc(read_int(data_buf), "z")

    result["MagX"] = calculate_mag(read_int(data_buf))
    result["MagY"] = calculate_mag(read_int(data_buf))
    result["MagZ"] = calculate_mag(read_int(data_buf))

    result["Temp_NTC"] = calculate_temp_NTC(read_int(data_buf))

    result["Time"] = convert_time(read_unsigned_long(data_buf))

    result["Temp_BMP180"] = read_double(data_buf)
    result["Press"] = calculate_press(read_double(data_buf))

    result["Lat"] = read_double(data_buf)
    result["Long"] = read_double(data_buf)

    result["Alt_GPS"] = read_double(data_buf)
    result["Course"] = read_double(data_buf)
    result["HDOP"] = read_signed_long(data_buf)
    result["Sats"] = read_unsigned_long(data_buf)

    result["CRC16"] = data_buf.read(2)

    result["Height"] = calculate_height(result["Press"],
                                        data_config["ground_pressure"],
                                        data_config["ground_temperature"])

    data_buf.seek(0)
    try:
        assert(verify_crc(result["CRC16"], data_buf.getvalue()[:-2]))
    except AssertionError:
        raise CRCValidationError("CRC validation failed.")
    import pprint
    pprint.pprint(result)

    return result


def easy_parse_line(line, data_config=None, verbose=True):
    """
    Parse data with a one-liner!

    Raises InvalidLine if ``line`` is not valid.
    """

    return parse_line(line)

    if data_config is None:
        data_config = copy(EXAMPLE_DATA_CONFIG)

    try:
        validate_line(line)
    except MalformedPacket:
        if verbose:
            line = line.replace("\n", "")
            print("[WARNING] Got malformed packet: {}".format(line))

        raise InvalidLine

    try:
        raw_data = parse_line(line)
    except ParseError as e:
        if verbose:
            print("[WARNING] Got a ParseError: {} on line {}".format(e, line))

        raise InvalidLine

    data = {}
    data["Time"] = raw_data["Time"]
    data["NTC"] = calculate_temp_NTC(raw_data["NTC"])
    data["Pressure"] = calculate_press(raw_data["Press"])
    data["Height"] = calculate_height(data["Pressure"],
                                      data_config["ground_pressure"],
                                      data_config["ground_temperature"])
    data["Gyroscope"] = calculate_gyr(raw_data["GyrZ"]) / 360 * 60  # RPM

    return data
