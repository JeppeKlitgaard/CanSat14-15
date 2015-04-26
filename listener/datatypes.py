

class Datatype(object):
    def __init__(self, time, raw_data):
        self.time = time
        self.raw_data = raw_data

    def __repr__(self):
        return "{}: {} {}".format(self.CLASSNAME, self.data, self.UNIT)


class TemperatureLM35(Datatype):
    CLASSNAME = "Temperature (LM35)"
    UNIT = "C"

    @property
    def celsius(self):
        voltage = self.raw_data / 1023 * 5
        temp = voltage / 0.01
        return temp

    @property
    def data(self):
        return self.celsius

