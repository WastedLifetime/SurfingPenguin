""" __init__.py: Initialization of the server """
import os
from flask import Flask
from src.config import ProductionConfig, DevelopmentConfig, StagingConfig
from flask_login import LoginManager
from flask_restplus import Api
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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
                          echo=True)

login_manager = LoginManager(surfing_penguin)
login_manager.login_view = 'login'
login_manager.init_app(surfing_penguin)


api = Api(surfing_penguin)

from src.surfing_penguin import models  # noqa: F401
Base.metadata.create_all(db_engine)
Session = sessionmaker(bind=db_engine)
session = Session()

from src.surfing_penguin import routes  # noqa
