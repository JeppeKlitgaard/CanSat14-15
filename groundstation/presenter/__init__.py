"""
Contains a Flask-based webserver in charge of presenting a website and
collected data to users connected via a webbrowser.
"""

__version__ = (0, 0, 1)

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["BOOTSTRAP_SERVE_LOCAL"] = True

Bootstrap(app)

from . import views  # noqa unused-import
