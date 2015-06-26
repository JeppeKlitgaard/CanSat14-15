"""
Contains the logic used by the presenter module.
"""

import json
import os

from groundstation.exceptions import ParseError
from groundstation.parse import easy_parse_line
from groundstation.utilities import convert_time
from groundstation.config import DATA_BASE_PATH, DATA_CONFIG_FILE

from flask import abort


def get_global_data_config():
    """
    Returns the data configuration as a python object.
    """
    data_config_path = os.path.abspath(os.path.join(DATA_BASE_PATH,
                                                    DATA_CONFIG_FILE))

    with open(data_config_path, "r") as f:
        data_config = json.load(f)

    return data_config


def _get_data_file(data_id):
    """
    Returns a ``str`` with the absolute path to the data-file associated
    with ``data_id``.
    """
    try:
        data_conf = _get_data_config(data_id)
        file_ = os.path.abspath(os.path.join(DATA_BASE_PATH,
                                             data_conf["file"]))
    except IndexError:
        abort(404)

    return file_


def _get_data_config(data_id):
    """
    Returns the dictionary associated with ``data_id``.
    """
    data_config = get_global_data_config()

    matches_type = [data for data in data_config if isinstance(data, dict)]
    matches = [data for data in matches_type if data["id"] == data_id]

    return matches[0]


def get_static_graph_data(data_id, force=False):
    """
    Returns a jsonified string of data to be sent along with a Response to a
    client connected to the static graph endpoint.
    """
    data_conf = _get_data_config(data_id)

    version = data_conf["protocol_version"]

    if version in ["portugal2015", "live"]:
        return _get_static_graph_data_portugal2015(data_id, data_conf, force)

    elif version in ["andoeya2015"]:
        return _get_static_graph_data_andoeya2015(data_id, data_conf, force)

    else:
        raise ValueError("Invalid 'version'.")


def _get_static_graph_data_portugal2015(data_id, data_conf, force=False):
    """
    Returns a jsonified string of data to be sent along with a Response to a
    client connected to the static graph endpoint.
    """
    data_temp_1 = []
    data_temp_2 = []
    data_press = []
    data_height = []
    data_gyro = []

    try:
        with open(_get_data_file(data_id), "r") as f:
            for line in f:
                    try:
                        values = easy_parse_line(line, data_config=data_conf,
                                                 version="portugal2015")

                        time = convert_time(values["Time"] - data_conf["start_time"])

                        data_temp_1.append([time, values["NTC"]])
                        data_temp_2.append([time, values["BMP180_Temp"]])
                        data_press.append([time, values["Pressure"]])
                        data_height.append([time, values["Height"]])
                        data_gyro.append([time, values["GyrZ"]])

                    except ParseError:
                        if not force:
                            raise

    except FileNotFoundError:
        abort(404)

    for lst in [data_temp_1, data_temp_2, data_press, data_height, data_gyro]:
        # Sort by time
        lst.sort(key=lambda x: x[0])

    data = {
        "NTC_Temp": data_temp_1,
        "BMP180_Temp": data_temp_2,
        "Press": data_press,
        "Height": data_height,
        "Gyro": data_gyro
    }

    json_data = json.dumps(data, separators=(",", ":"))

    return json_data


def _get_static_graph_data_andoeya2015(data_id, data_conf, force=False):
    """
    Returns a jsonified string of data to be sent along with a Response to a
    client connected to the static graph endpoint.
    """
    data_temp = []
    data_press = []
    data_height = []
    data_gyro = []

    try:
        with open(_get_data_file(data_id), "r") as f:
            for line in f:
                    try:
                        values = easy_parse_line(line, data_config=data_conf,
                                                 version="andoeya2015")

                        time = convert_time(values["Time"] - data_conf["start_time"])

                        data_temp.append([time, values["NTC"]])
                        data_press.append([time, values["Pressure"]])
                        data_height.append([time, values["Height"]])
                        data_gyro.append([time, values["GyrZ"]])

                    except ParseError:
                        if not force:
                            raise

    except FileNotFoundError:
        abort(404)

    for lst in [data_temp, data_press, data_height, data_gyro]:
        # Sort by time
        lst.sort(key=lambda x: x[0])

    data = {
        "NTC_Temp": data_temp,
        "Press": data_press,
        "Height": data_height,
        "Gyro": data_gyro
    }

    json_data = json.dumps(data, separators=(",", ":"))

    return json_data
