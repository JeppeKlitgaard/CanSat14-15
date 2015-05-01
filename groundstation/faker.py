"""
Generates fake data.
Used to test the rest of the groundstation module when no CanSat data is
available.
"""

import time
import random
from .parse import HEAD, HEAD_SEP, DATA_SEP, FIELD_SEP
from .config import FAKER, GENERAL


class Faker(object):
    """Generates fake data."""
    FIELDS = ["NTC",
              "LM35",
              "Press",
              "AccX", "AccY", "AccZ",
              "GyrX", "GyrY", "GyrZ",
              "MagX", "MagY", "MagZ",
              "Lat", "Long", "Alt", "Cour", "Speed", "Sat"]

    ABS_FIELDS = FIELDS

    RAND_MIN = FAKER["min_value"]
    RAND_MAX = FAKER["max_value"]

    def __init__(self, data_interval=0.1, verbose=True,
                 malformed_line_chance=0):
        self.data_interval = data_interval
        self.last_data_read_time = 0
        self.file_handle = open(GENERAL["com_file"], "w")
        self.verbose = verbose
        self.malformed_line_chance = malformed_line_chance
        self.start_time = time.time()

    def start(self):
        """
        Starts the faker.
        """
        while True:
            self.write()

    def _gen_fake_line(self):
        """
        Generates a single, fake line.
        Has a chance of writing a malformed line, depending on the
        ``malformed_line_chance`` attribute.
        """
        if random.random() < self.malformed_line_chance:
            return "I am a malformed packet, yadaaa!\n"

        line = HEAD + HEAD_SEP

        fields = []
        for field in self.FIELDS:
            num = str(random.randint(self.RAND_MIN, self.RAND_MAX))
            if field in self.ABS_FIELDS:  # Some values must be positive
                num = str(abs(int(num)))
            fields.append(field + FIELD_SEP + num)

        fields.append("Time" + FIELD_SEP + str(time.time() - self.start_time))

        line += DATA_SEP.join(fields)

        line += "\n"

        return line

    def write(self):
        """
        Writes a single line of fake data, blocking the appropriate amount of
        time.
        """
        now = time.time()
        if now < self.last_data_read_time + self.data_interval:
            time.sleep((self.last_data_read_time + self.data_interval) - now)

        self.last_data_read_time = time.time()

        line = self._gen_fake_line()
        self.file_handle.write(line)
        self.file_handle.flush()

        if self.verbose:
            print(line, end="")


if __name__ == '__main__':
    faker = Faker(data_interval=FAKER["data_interval"],
                  malformed_line_chance=FAKER["malformed_line_chance"])
    faker.start()
