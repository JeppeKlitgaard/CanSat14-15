import json
import argparse
import os
from listener.config import MIN_TIME, MAX_TIME, PRESSURE_AVERAGE_AMOUNT
from listener.replayer import Replayer
from listener.utilities import convert_time, average
from listener.calculate import (calculate_temp_NTC, calculate_press,
                                calculate_height, calculate_gyr)
from collections import deque
from io import StringIO


parser = argparse.ArgumentParser(prog="Replayer",
                                 description="Replay a CanSat log file for "
                                             "listener.")

parser.add_argument("input_file")

args = parser.parse_args()

input_file = os.path.abspath(args.input_file)
input_handle = open(input_file, "r")

out_file = "static.json"
out_handle = open(out_file, "w")

replayer = Replayer(MIN_TIME, MAX_TIME, input_handle, StringIO(),
                    False, True)

full_data = replayer.start()

last_pressure_values = deque(maxlen=PRESSURE_AVERAGE_AMOUNT)

data_temperature = []
data_pressure = []
data_height = []
data_gyro = []

for datapoint in full_data:
    if not MIN_TIME <= datapoint["Time"] <= MAX_TIME:
        continue  # Skip

    pressure = calculate_press(datapoint["Press"])
    last_pressure_values.append(pressure)

    time = convert_time(datapoint["Time"] - MIN_TIME)
    data_temperature.append([time, calculate_temp_NTC(datapoint["NTC"])])

    pressure = average(last_pressure_values)
    data_pressure.append([time, pressure])

    data_height.append([time, calculate_height(pressure)])

    data_gyro.append([time, calculate_gyr(datapoint["GyrZ"])])

all_data = {
    "Temp": data_temperature,
    "Press": data_pressure,
    "Height": data_height,
    "Gyro": data_gyro
}

out_handle.write(json.dumps(all_data))

input_handle.close()
out_handle.close()
