"""
Contains functions and classes used to parse, handle, validate and interpret
data received from the CanSat (or Faker).
"""

from .exceptions import ParseError, MalformedPacket, InvalidLine
from .calculate import (calculate_temp_NTC, calculate_press, calculate_height,
                        calculate_gyr)
from .config import EXAMPLE_DATA_CONFIG

from copy import copy

import re

HEAD = "SGCanScience"
HEAD_SEP = ">"  # Separates Head of datastring.
DATA_SEP = "|"  # Separates data-points of datastring.
FIELD_SEP = ":"  # Separates key and value in a data field.
REQUIRED_FIELDS = ["Time", "Press", "NTC", "GyrX", "GyrY", "GyrZ",
                   "AccX", "AccY", "AccZ", "MagX", "MagY", "MagZ", "Lat",
                   "Long", "Sat"]

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


def easy_parse_line(line, data_config=None, verbose=True):
    """
    Parse data with a one-liner!

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
    data["Pressure"] = calculate_press(raw_data["Press"])
    data["Height"] = calculate_height(data["Pressure"],
                                      data_config["ground_pressure"],
                                      data_config["ground_temperature"])
    data["Gyroscope"] = calculate_gyr(raw_data["GyrZ"]) / 360 * 60  # RPM

    return data
