"""__init__.py: Initialization of the server"""
import os
from flask import Flask
from src.config import Config, ProductionConfig, DevelopmentConfig , StagingConfig
from flask_restplus import Api
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

surfing_penguin = Flask(__name__)
ENV=os.environ.get('ENV')
if ENV == "Staging":
    surfing_penguin.config.from_object(StagingConfig)
if ENV == "Development":
    surfing_penguin.config.from_object(DevelopmentConfig)
if ENV == "Production":
    surfing_penguin.config.from_object(ProductionConfig)

db_engine = create_engine(surfing_penguin.config['SQLALCHEMY_DATABASE_URI'], echo=False)

api = Api(surfing_penguin)

from src.surfing_penguin import models  # noqa: F401
Base.metadata.create_all(db_engine)
Session = sessionmaker(bind=db_engine)
session = Session()

from src.surfing_penguin import routes
