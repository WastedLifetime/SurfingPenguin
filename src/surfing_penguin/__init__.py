"""__init__.py: Initialization of the server"""

from flask import Flask
from config import Config
from sqlalchemy import create_engine
from flask_restplus import Api

surfing_penguin = Flask(__name__)
surfing_penguin.config.from_object(Config)
db_engine = create_engine('sqlite:///:memory:', echo=False)
api = Api(surfing_penguin)

from surfing_penguin import routes, models  # noqa: F401
