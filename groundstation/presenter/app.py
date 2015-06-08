from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["BOOTSTRAP_SERVE_LOCAL"] = True

Bootstrap(app)

from . import views  # noqa unused-import
