"""
Contains the exceptions used by the groundstation module.
"""


class GroundstationError(Exception):
    """
    General exception used as an ABC by the groundstation.
    """
    pass


class ParseError(GroundstationError):
    """
    Exception raised when an error during parsing occurs.
    """
    pass


class CRCValidationError(ParseError):
    """
    Exception raised when the CRC calculations do not match.
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
