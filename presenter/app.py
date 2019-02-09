"""
This module instantiates the flask application and
applies the configuration file as well as the extensions.

It also sets up the database and the OEmbed cache.
"""

from flask import Flask
from flask_bootstrap import Bootstrap

from micawber import bootstrap_basic
from micawber.cache import Cache as OEmbedCache

from playhouse.flask_utils import FlaskDB

from . import secret_config

app = Flask(__name__)

app.config.from_object(secret_config)
app.config["DATABASE"] = "sqliteext:///presenter.db"

Bootstrap(app)

flask_db = FlaskDB(app)
database = flask_db.database

oembed_providers = bootstrap_basic(OEmbedCache)

from .models import Entry

database.create_tables([Entry], safe=True)
