"""
This module instantiates the flask application and
applies the configuration file as well as the extensions.

It also sets up the database and the OEmbed cache.
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension

from micawber import bootstrap_basic
from micawber.cache import Cache as OEmbedCache

from playhouse.flask_utils import FlaskDB

from .models import Entry

from . import config
from . import secret_config

app = Flask(__name__)

app.config.from_object(config)
app.config.from_object(secret_config)

Bootstrap(app)
DebugToolbarExtension(app)

flask_db = FlaskDB(app)
database = flask_db.database

oembed_providers = bootstrap_basic(OEmbedCache)

database.create_tables([Entry], safe=True)
