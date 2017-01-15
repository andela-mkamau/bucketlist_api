from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    """
    Application factory

    This creates a single instance of the Flask app using the given
    configuration. It initialises extensions and registers blueprints.

    :param config_name: configuration that maps to a Config class
    :return: a Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    # register api blueprint
    from app import api as api_blueprint
    app.register_blueprint(api_blueprint.api, url_prefix='/api')

    return app

