import argparse
import os
import sys
import csv

from groundstation.parse import easy_parse_line
from groundstation.config import EXAMPLE_DATA_CONFIG
from presenter.logic import _get_data_config

parser = argparse.ArgumentParser(prog="Excelify Log",
                                 description="Turn CanSat log files into an"
                                 "Excel-digestable CSV file.")

parser.add_argument("input_file")
parser.add_argument("-o", dest="output_file")
parser.add_argument("-c", dest="data_config_id")

args = parser.parse_args()

input_file = os.path.abspath(args.input_file)
input_handle = open(input_file, "r")

if args.output_file:
    output_file = os.path.abspath(args.output_file)
    output_handle = open(output_file, "w")
else:
    output_handle = sys.stdout

if args.data_config_id:
    data_config = _get_data_config(args.data_config_id)
else:
    data_config = EXAMPLE_DATA_CONFIG

datas = easy_parse_line(input_handle.readline(),
                        version=data_config["protocol_version"]).keys()
input_handle.seek(0)

csvwriter = csv.DictWriter(output_handle, datas)
csvwriter.writeheader()

for line in input_handle:
    data = easy_parse_line(line, data_config,
                           version=data_config["protocol_version"])

    csvwriter.writerow(data)


input_handle.close()
output_handle.close()
