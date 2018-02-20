"""__init__.py: Initialization of the server"

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

surfing_penguin = Flask(__name__)
surfing_penguin.config.from_object(Config)
db = SQLAlchemy(surfing_penguin)
migrate = Migrate(surfing_penguin, db)

from surfing_penguin import routes, models
