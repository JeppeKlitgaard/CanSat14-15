"""
Contains a Flask-based webserver in charge of presenting a website and
collected data to users connected via a webbrowser.
"""

__version__ = (0, 0, 1)

from .app import app, database
from .models import Entry

from .config import HOST, PORT


def run():
    """
    Runs the presenter module.
    """
    # pylint: disable=unused-variable
    from . import views  # noqa
    # pylint: enable=unused-variable

    database.create_tables([Entry], safe=True)

    app.run(use_reloader=False, host=HOST, port=PORT)


if __name__ == '__main__':
    run()
