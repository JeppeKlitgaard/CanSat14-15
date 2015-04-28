from flask import render_template, send_from_directory, abort
from . import app
import os
from ..config import GENERAL
from ..parse import easy_parse_line
import json

data_config_path = os.path.abspath(os.path.join(GENERAL["data_base_path"],
                                                GENERAL["data_config"]))
with open(data_config_path, "r") as f:
    data_config = json.load(f)


def _get_data_file(data_id):
    matches_type = [data for data in data_config if isinstance(data, dict)]
    matches = [data for data in matches_type if data["id"] == data_id]

    try:
        file_ = os.path.abspath(os.path.join(GENERAL["data_base_path"],
                                             matches[0]["file"]))
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
        return data_config
    return dict(get_dropdown_data=get_dropdown_data)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/live")
def live():
    return render_template("live.html")


@app.route("/graph/<data_id>")
def graph(data_id):
    with open(_get_data_file(data_id), "r") as f:
        data_temp = []
        data_press = []
        data_height = []
        data_gyro = []

        for line in f:
            values = easy_parse_line(line)
            data_temp.append([values["Time"], values["NTC"]])
            data_press.append([values["Time"], values["Pressure"]])
            data_height.append([values["Time"], values["Height"]])
            data_gyro.append([values["Time"], values["Gyroscope"]])

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
    return render_template("replay.html", data_id=data_id)
