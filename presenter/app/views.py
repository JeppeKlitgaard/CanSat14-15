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
@app.route("/graph")
def graph():
    return render_template("graph.html")


@app.route("/graph_static_droptest")
def graph_static_droptest():
    return render_template("graph_static_droptest.html")


@app.route("/graph_static_rocket")
def graph_static_rocket():
    return render_template("graph_static_rocket.html")
