"""
Contains the exceptions used by the groundstation module.
"""


class ParseError(Exception):
    """
    Exception raised when an error during parsing occurs.
    """
    pass


class MalformedPacket(ParseError):
    """
    Exception raised when a malformed packet is received,
    probably due to noise on the radio frequency.
    """
    pass


class InvalidLine(ParseError):
    """
    Exception raised when an invalid line is found.
    """
    pass
