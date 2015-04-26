__version__ = (0, 0, 1)

from flask import Flask
from flask_bootstrap import Bootstrap

from ..config import PRESENTER

import json
import os

data_config_path = os.path.abspath(os.path.join(PRESENTER["data_base_path"],
                                                PRESENTER["data_config"]))

app = Flask(__name__)
app.config["BOOTSTRAP_SERVE_LOCAL"] = True

with open(data_config_path, "r") as f:
    app.config["data"] = json.load(f)

Bootstrap(app)

from . import views
