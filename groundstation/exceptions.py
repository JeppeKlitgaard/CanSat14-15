class ParseError(Exception):
    pass


class MalformedPacket(ParseError):
    pass


class InvalidLine(ParseError):
    pass
