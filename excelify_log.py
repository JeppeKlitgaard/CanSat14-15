import argparse
import os
import sys
import csv
from collections import deque
from listener.parse import validate_line, parse_line
from listener.exceptions import MalformedPacket, ParseError
from listener.calculate import (calculate_temp_NTC, calculate_temp_LM35,
                                calculate_press, calculate_gyr,
                                calculate_acc_x, calculate_acc_y,
                                calculate_acc_z, calculate_mag)
from listener.config import MIN_TIME, MAX_TIME, PRESSURE_AVERAGE_AMOUNT
from listener.utilities import average, convert_time

DATAS = ["Time", "Pressure", "Average_Pressure", "LM35", "NTC", "GyrX",
         "GyrY", "GyrZ", "AccX",
         "AccY", "AccZ", "MagX", "MagY", "MagZ", "Latitude", "Longitude",
         "Altitude", "Course", "Speed", "Satellites"]

parser = argparse.ArgumentParser(prog="Excelify Log",
                                 description="Turn CanSat log files into an"
                                 "Excel-digestable CSV file.")

parser.add_argument("input_file")
parser.add_argument("-o", dest="output_file")

args = parser.parse_args()

input_file = os.path.abspath(args.input_file)
input_handle = open(input_file, "r")

if args.output_file:
    output_file = os.path.abspath(args.output_file)
    output_handle = open(output_file, "w")
else:
    output_handle = sys.stdout

csvwriter = csv.DictWriter(output_handle, DATAS)
csvwriter.writeheader()

last_pressure_values = deque(maxlen=PRESSURE_AVERAGE_AMOUNT)

for line in input_handle:
    try:
        validate_line(line)
        data = parse_line(line)
    except (MalformedPacket, ParseError):
        print("Skipped a malformed line.")
        continue

    try:
        if not MIN_TIME <= data["Time"] <= MAX_TIME:
            continue

        # PRESSURE AVERAGING
        pressure = calculate_press(data["Press"])
        last_pressure_values.append(pressure)

        try:
            csvwriter.writerow({
                "Time": convert_time(data["Time"] - MIN_TIME),
                "Pressure": pressure,
                "Average_Pressure": average(last_pressure_values),
                "LM35": calculate_temp_LM35(data["LM35"]),
                "NTC": calculate_temp_NTC(data["NTC"]),
                "GyrX": calculate_gyr(data["GyrX"]),
                "GyrY": calculate_gyr(data["GyrY"]),
                "GyrZ": calculate_gyr(data["GyrZ"]),
                "AccX": calculate_acc_x(data["AccX"]),
                "AccY": calculate_acc_y(data["AccY"]),
                "AccZ": calculate_acc_z(data["AccZ"]),
                "MagX": calculate_mag(data["MagX"]),
                "MagY": calculate_mag(data["MagY"]),
                "MagZ": calculate_mag(data["MagZ"]),
                "Latitude": data["Lat"],
                "Longitude": data["Long"],
                "Course": data["Cour"],
                "Speed": data["Speed"],
                "Satellites": data["Sat"]
            })
        except Exception as e:
            print("Got error, ignored line: {}".format(e))
    except KeyError:
        continue


input_handle.close()
output_handle.close()
