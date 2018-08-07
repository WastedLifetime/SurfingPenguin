from flask import Blueprint
from flask_restplus import Api
from src.surfing_penguin import __version__

api_prefix = "/api/"+__version__[0:3]
blueprint = Blueprint("api",
                      __name__,
                      url_prefix=api_prefix)

api = Api(blueprint,
          version=__version__[0:3],
          title="Surfing Penguin API",
          doc="/doc")

from src.surfing_penguin.API import user_api, survey_api  # noqa
