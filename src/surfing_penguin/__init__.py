""" __init__.py: Initialization of the server """
import os
from flask import Flask
from src.config import ProductionConfig, DevelopmentConfig, StagingConfig
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: refactor this file and add create_app(config) function
Base = declarative_base()

surfing_penguin = Flask(__name__)

ENV = os.environ.get('ENV')

if ENV == "Staging":
    surfing_penguin.config.from_object(StagingConfig)
elif ENV == "Production":
    surfing_penguin.config.from_object(ProductionConfig)
else:
    surfing_penguin.config.from_object(DevelopmentConfig)


db_engine = create_engine(surfing_penguin
                          .config['SQLALCHEMY_DATABASE_URI'],
                          echo=False)

def create_login_manager(app):
    login_manager = LoginManager(surfing_penguin)
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    return login_manager

login_manager = create_login_manager(surfing_penguin)

from src.surfing_penguin import models  # noqa: F401

def create_db_session(db_engine):
    Base.metadata.create_all(db_engine)
    Session = sessionmaker(bind=db_engine)
    session = Session()
    return session

session = create_db_session(db_engine)

from src.surfing_penguin import routes  # noqa
surfing_penguin.register_blueprint(routes.blueprint)
