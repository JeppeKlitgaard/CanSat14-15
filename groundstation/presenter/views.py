from flask import render_template, send_from_directory
from . import app
import os
from ..config import PRESENTER
import json

data_config_path = os.path.abspath(os.path.join(PRESENTER["data_base_path"],
                                                PRESENTER["data_config"]))


@app.context_processor
def dropdown_processor():
    """
    Context processor that makes the get_dropdown_data function
    available to all templates.
    """
    def get_dropdown_data():
        with open(data_config_path, "r") as f:
            data = json.load(f)

        return data
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
    return render_template("graph.html", data_id=data_id)


@app.route("/replay/<data_id>")
def replay(data_id):
    return render_template("replay.html", data_id=data_id)
