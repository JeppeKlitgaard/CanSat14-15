import os


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


def convert_time(time):
    return time / 1000


def average(iterable):
    return sum(iterable) / len(iterable)
