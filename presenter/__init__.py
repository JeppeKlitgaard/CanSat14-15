"""
Contains a Flask-based webserver in charge of presenting a website and
collected data to users connected via a webbrowser.
"""

__version__ = (0, 0, 1)

from .app import app

from .config import DevelopmentConfig, ProductionConfig

from flask_debugtoolbar import DebugToolbarExtension


def run_dev():
    """
    Runs the presenter module in developer mode.
    """
    # pylint: disable=unused-variable
    from . import views  # noqa
    # pylint: enable=unused-variable

    app.config.from_object(DevelopmentConfig)

    toolbar = DebugToolbarExtension(app)

    app.run(use_reloader=False, host=DevelopmentConfig.HOST,
            port=DevelopmentConfig.PORT)


def run_prod():
    """
    Runs the presenter module in production mode.
    """
    # pylint: disable=unused-variable
    from . import views  # noqa
    # pylint: enable=unused-variable

    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from presenter import app

    app.config.from_object(ProductionConfig)

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(ProductionConfig.PORT)

    IOLoop.instance().start()

if __name__ == '__main__':
    run()
