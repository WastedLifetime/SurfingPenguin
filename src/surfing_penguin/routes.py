from flask import Blueprint
from flask_restplus import Api
from src.surfing_penguin import __version__

ver = __version__[0:3]
api_prefix = "/api/"+ver+"/"
blueprint = Blueprint("api",
                      __name__,
                      url_prefix=api_prefix)

api = Api(blueprint,
          version="0.1",
          title="Surfing Penguin API",
          doc="/doc")

from src.surfing_penguin.API import User, Survey
