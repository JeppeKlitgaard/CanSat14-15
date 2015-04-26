from flask import render_template, send_from_directory
from . import app
import os


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


# TODO REMOVE
@app.route("/graph_static_droptest")
def graph_static_droptest():
    return render_template("graph_static_droptest.html")


@app.route("/graph_static_rocket")
def graph_static_rocket():
    return render_template("graph_static_rocket.html")
