"""
Contains functions and classes used to parse, handle, validate and interpret
data received from the CanSat (or Faker).
"""

from .exceptions import ParseError, MalformedPacket, InvalidLine
from .calculate import (calculate_temp_NTC, calculate_temp_LM35,
                        calculate_press, calculate_height,
                        calculate_gyr, calculate_acc, calculate_mag)
from .config import EXAMPLE_DATA_CONFIG

from copy import copy

import re

HEAD = "SGCanScience"
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
    if not VALID_PATTERN.match(line):
        raise MalformedPacket("Got malformed packet: {}".format(line))


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


def parse_line(line):
    """Parses a line of output from the CanSat."""
    line = line.replace("\n", "")

    try:
        head, data_string = line.split(HEAD_SEP)
        if head != HEAD:
            raise ParseError("Got a wrong head.")

    except ValueError:
        raise ParseError("Wrong amount of HEAD_SEP's.")

    data_fields = data_string.split(DATA_SEP)

    data_fields = [x for x in data_fields if x]

    data = {}
    for data_field in data_fields:
        try:
            key, value = data_field.split(FIELD_SEP)
        except ValueError:
            raise ParseError("Wrong amount of FIELD_SEP's.")
        key = handle_key(key)
        try:
            value = handle_value(value)
        except ValueError:
            raise ParseError("Failed to handle value.")
        data[key] = value

    for required_field in REQUIRED_FIELDS:
        if required_field not in data.keys():
            raise ParseError(("A field '{}' went missing!"
                              .format(required_field)))

    return data


def easy_parse_line(*args, **kwargs):
    """
    Parse data with a one-liner!

    Raises InvalidLine if ``line`` is not valid.
    """
    version = kwargs["version"]
    del kwargs["version"]

    if version in ["live", "portugal2015"]:
        return easy_parse_line_portugal2015(*args, **kwargs)

    elif version in ["andoeya2015"]:
        return easy_parse_line_andoeya2015(*args, **kwargs)

    else:
        raise ValueError("Invalid 'version'.")


def easy_parse_line_portugal2015(line, data_config=None, verbose=True):
    """
    Parse data with a one-liner! (Portugal 2015 format)

    Raises InvalidLine if ``line`` is not valid.
    """

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

    data["BMP180_Temp"] = raw_data["Temp"]

    data["Pressure"] = calculate_press(raw_data["Press"], version="portugal2015")

    data["GyrX"] = calculate_gyr(raw_data["GyrX"]) / 360 * 60  # RPM
    data["GyrY"] = calculate_gyr(raw_data["GyrY"]) / 360 * 60  # RPM
    data["GyrZ"] = calculate_gyr(raw_data["GyrZ"]) / 360 * 60  # RPM

    data["AccX"] = calculate_acc(raw_data["AccX"], "x")
    data["AccY"] = calculate_acc(raw_data["AccY"], "y")
    data["AccZ"] = calculate_acc(raw_data["AccZ"], "z")

    data["MagX"] = calculate_mag(raw_data["MagX"])
    data["MagY"] = calculate_mag(raw_data["MagY"])
    data["MagZ"] = calculate_mag(raw_data["MagZ"])

    data["Height"] = calculate_height(data["Pressure"],
                                      data_config["ground_pressure"],
                                      data_config["ground_temperature"])

    data["Latitude"] = raw_data["Lat"]
    data["Longitude"] = raw_data["Long"]
    data["Satelittes"] = raw_data["Sat"]

    return data


def easy_parse_line_andoeya2015(line, data_config=None, verbose=True):
    """
    Parse data with a one-liner! (Andoeya 2015 format)

    Raises InvalidLine if ``line`` is not valid.
    """

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

    data["Pressure"] = calculate_press(raw_data["Press"],
                                       version="andoeya2015")

    data["LM35"] = calculate_temp_LM35(raw_data["LM35"])
    data["NTC"] = calculate_temp_NTC(raw_data["NTC"])

    data["GyrX"] = calculate_gyr(raw_data["GyrX"]) / 360 * 60  # RPM
    data["GyrY"] = calculate_gyr(raw_data["GyrY"]) / 360 * 60  # RPM
    data["GyrZ"] = calculate_gyr(raw_data["GyrZ"]) / 360 * 60  # RPM

    data["AccX"] = calculate_acc(raw_data["AccX"], "x")
    data["AccY"] = calculate_acc(raw_data["AccY"], "y")
    data["AccZ"] = calculate_acc(raw_data["AccZ"], "z")

    data["MagX"] = calculate_mag(raw_data["MagX"])
    data["MagY"] = calculate_mag(raw_data["MagY"])
    data["MagZ"] = calculate_mag(raw_data["MagZ"])

    data["Height"] = calculate_height(data["Pressure"],
                                      data_config["ground_pressure"],
                                      data_config["ground_temperature"])

    data["Latitude"] = raw_data["Lat"]
    data["Longitude"] = raw_data["Long"]
    data["GPS_Altitude"] = raw_data["Alt"]
    data["Course"] = raw_data["Cour"]
    data["Speed"] = raw_data["Speed"]
    data["Satelittes"] = raw_data["Sat"]

    return data
