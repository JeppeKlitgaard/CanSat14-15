from .datatypes import TemperatureLM35
from .exceptions import ParseError, MalformedPacket

import re

HEAD = "SGCanScience"
HEAD_SEP = ">"  # Separates Head of datastring.
DATA_SEP = "|"  # Separates data-points of datastring.
FIELD_SEP = ":"  # Separates key and value in a data field.
REQUIRED_FIELDS = ["Time", "Press", "LM35", "NTC", "GyrX", "GyrY", "GyrZ",
                   "AccX", "AccY", "AccZ", "MagX", "MagY", "MagZ", "Lat",
                   "Long", "Alt", "Cour", "Speed", "Sat"]

VALID_PATTERN = re.compile(r"SGCanScience>(\w+:[-.0-9]+\|?)+")


def validate_line(line):
    if not VALID_PATTERN.match(line):
        raise MalformedPacket("Got malformed packet: {}".format(line))


def handle_key(key):
    return key


def handle_value(value):
    value = value.replace("\n", "")
    value = float(value)

    return value


def parse_line(line):
    """Parses a line of output from the Arduino."""
    line = line.replace("\n", "")

    try:
        head, data_string = line.split(HEAD_SEP)
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
            raise ParseError("A field went missing!")

    return data
