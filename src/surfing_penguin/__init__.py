""" __init__.py: Initialization of the server """
import os
from flask import Flask
from src.config import ProductionConfig, DevelopmentConfig, StagingConfig


__version__ = '0.1.0'


def get_config():
    ENV = os.environ.get('ENV')

    if ENV == "Staging":
        config = StagingConfig
    elif ENV == "Production":
        config = ProductionConfig
    else:
        config = DevelopmentConfig

    return config


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    from . import extensions
    extensions.init_app(app)
    return app


config = get_config()
surfing_penguin = create_app(config)
from src.surfing_penguin import routes  # noqa
surfing_penguin.register_blueprint(routes.blueprint)
