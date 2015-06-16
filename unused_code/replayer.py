import argparse
import os
import time

from .config import MIN_TIME, MAX_TIME, COM_FILE
from .utilities import convert_time
from .parse import validate_line, parse_line
from .exceptions import MalformedPacket, ParseError


class Replayer(object):
    def __init__(self, min_time, max_time, input_handle, com_handle,
                 real_time=True, return_full_data=False):
        self.min_time = min_time
        self.max_time = max_time
        self.input_handle = input_handle
        self.com_handle = com_handle
        self.real_time = real_time
        self.return_full_data = return_full_data

    def _get_elapsed_time(self):
        return time.time() - self.start_time

    def start(self):
        self.start_time = time.time()
        full_data = []
        for line in self.input_handle:

            try:
                validate_line(line)
            except MalformedPacket:
                print("Malformed packet. Skipping.")
                continue

            try:
                data = parse_line(line)
            except ParseError as e:
                print("Got ParseError, skipping: {}".format(e))
                continue

            if not self.min_time <= data["Time"] <= self.max_time:
                print("Not within allowed time-frame. Skipping.")
                continue

            time_since_launch = convert_time(data["Time"] - self.min_time)
            elapsed_time = self._get_elapsed_time()

            time_to_sleep = time_since_launch - elapsed_time
            if time_to_sleep > 0 and self.real_time:
                time.sleep(time_since_launch - elapsed_time)

            self.com_handle.write(line)
            self.com_handle.flush()

            print(line)
            print(data)

            full_data.append(data)

        return full_data


if __name__ == '__main__':
    desc = "Replay a CanSat log file for listener."
    parser = argparse.ArgumentParser(prog="Replayer",
                                     description=desc)

    parser.add_argument("input_file")

    args = parser.parse_args()

    input_file = os.path.abspath(args.input_file)
    input_handle = open(input_file, "r")

    com_handle = open(COM_FILE, "w")
    replayer = Replayer(MIN_TIME, MAX_TIME, input_handle, com_handle)
    replayer.start()
