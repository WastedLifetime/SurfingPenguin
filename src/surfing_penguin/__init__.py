"""__init__.py: Initialization of the server"""

from flask import Flask
from config import Config
from flask_restplus import Api
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

surfing_penguin = Flask(__name__)
surfing_penguin.config.from_object(Config)
db_engine = create_engine('sqlite:///:memory:', echo=False)

authorizations = {
    'apikey' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'X-API-KEY'
    }
}

api = Api(surfing_penguin, authorizations=authorizations)

from surfing_penguin import models  # noqa: F401
Base.metadata.create_all(db_engine)
Session = sessionmaker(bind=db_engine)
session = Session()

from surfing_penguin import routes
