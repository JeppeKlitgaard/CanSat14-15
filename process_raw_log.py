from groundstation.config import GENERAL
from groundstation.parse import easy_parse_line
from groundstation.exceptions import InvalidLine
import argparse
import os

parser = argparse.ArgumentParser(prog="Raw Log Processor",
                                 description="Processes a raw CanSat log file"
                                             " and places to processed file in"
                                             " the data folder.")

parser.add_argument("input_file")
parser.add_argument("out_name")
parser.add_argument("-s", "--start-time", type=int, default=0,
                    help="set start time")
parser.add_argument("-e", "--end-time", type=int, default=-1,
                    help="set end time")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")

args = parser.parse_args()

# Set up file handles.
input_file = os.path.abspath(args.input_file)
input_handle = open(input_file, "r")

out_file = os.path.abspath(os.path.join(GENERAL["data_base_path"],
                                        args.out_name + ".log"))
out_handle = open(out_file, "w")

for line in input_handle:
    try:
        data = easy_parse_line(line, verbose=args.verbose)
    except InvalidLine:
        continue

    if data["Time"] < args.start_time:
        if args.verbose:
            print("Skipped line due to time.")
        continue

    if args.end_time != -1 and data["Time"] > args.end_time:
        if args.verbose:
            print("Skipped line due to time.")
        continue

    out_handle.write(line)
