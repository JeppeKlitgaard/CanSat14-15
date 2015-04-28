__version__ = (0, 0, 1)

from flask import Flask
from flask_bootstrap import Bootstrap

import os

app = Flask(__name__)
app.config["BOOTSTRAP_SERVE_LOCAL"] = True

Bootstrap(app)

from . import views
