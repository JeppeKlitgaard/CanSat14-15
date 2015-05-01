"""
Contains the views and routes used by the Flask-webserver.
"""

from flask import render_template, send_from_directory, abort
from . import app
import os
from ..config import GENERAL
from ..parse import easy_parse_line
from ..utilities import convert_time
import json

data_config_path = os.path.abspath(os.path.join(GENERAL["data_base_path"],
                                                GENERAL["data_config"]))
with open(data_config_path, "r") as f:
    data_config = json.load(f)


def _get_data_config(data_id):
    """
    Returns the dictionary associated with ``data_id``.
    """
    matches_type = [data for data in data_config if isinstance(data, dict)]
    matches = [data for data in matches_type if data["id"] == data_id]

    return matches[0]


def _get_data_file(data_id):
    """
    Returns a ``str`` with the absolute path to the data-file associated
    with ``data_id``.
    """
    data_conf = _get_data_config(data_id)

    try:
        file_ = os.path.abspath(os.path.join(GENERAL["data_base_path"],
                                             data_conf["file"]))
    except IndexError:
        abort(404)

    return file_


@app.context_processor
def dropdown_processor():
    """
    Context processor that makes the get_dropdown_data function
    available to all templates.
    """
    def get_dropdown_data():
        """
        Returns dropdown data.
        """
        return data_config
    return dict(get_dropdown_data=get_dropdown_data)


@app.route("/favicon.ico")
def favicon():
    """
    Route in charge of finding the favicon.ico.
    """
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/about")
def about():
    """
    Renders the about page.
    """
    return render_template("about.html")


@app.route("/")
@app.route("/index")
def index():
    """
    Renders the index page.
    """
    return render_template("index.html")


@app.route("/live")
def live():
    """
    Renders the live page.
    """
    return render_template("live.html")


@app.route("/graph/<data_id>")
def graph(data_id):
    """
    Renders the graph page using a ``data_id``.
    """
    try:
        with open(_get_data_file(data_id), "r") as f:
            data_conf = _get_data_config(data_id)

            data_temp = []
            data_press = []
            data_height = []
            data_gyro = []

            for line in f:
                values = easy_parse_line(line, data_config=data_conf)

                time = convert_time(values["Time"] - data_conf["start_time"])

                data_temp.append([time, values["NTC"]])
                data_press.append([time, values["Pressure"]])
                data_height.append([time, values["Height"]])
                data_gyro.append([time, values["Gyroscope"]])

    except FileNotFoundError:
        abort(404)

    for lst in [data_temp, data_press, data_height, data_gyro]:
        # Sort by time
        lst.sort(key=lambda x: x[0])

    data = {
        "Temp": data_temp,
        "Press": data_press,
        "Height": data_height,
        "Gyro": data_gyro
    }

    json_data = json.dumps(data, separators=(",", ":"))

    return render_template("graph.html", graph_data=json_data)


@app.route("/replay/<data_id>")
def replay(data_id):
    """
    Renders the replay page using a ``data_id``.
    """
    return render_template("replay.html", data_id=data_id)
