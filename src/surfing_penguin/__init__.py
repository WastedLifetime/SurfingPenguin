"""__init__.py: Initialization of the server"""

from flask import Flask
from src.config import Config
from flask_restplus import Api
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

surfing_penguin = Flask(__name__)
surfing_penguin.config.from_object(Config)
db_engine = create_engine('postgres://tirbevwnotwfvq:504b36902c0cb58897c0e04ffd10af7384fd480949927d3e40d3b0108f53dfba@ec2-54-163-240-54.compute-1.amazonaws.com:5432/d7t8l4b4r9adoj', echo=False)

api = Api(surfing_penguin)

from src.surfing_penguin import models  # noqa: F401
Base.metadata.create_all(db_engine)
Session = sessionmaker(bind=db_engine)
session = Session()

from src.surfing_penguin import routes
