"""
Contains the configuration parameters used by the presenter module.
"""


class Config(object):
    """
    ABC for flask configurations.
    """
    DEBUG = True

    SITE_WIDTH = 800

    HOST = "0.0.0.0"
    PORT = 80

    BOOTSTRAP_SERVE_LOCAL = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
