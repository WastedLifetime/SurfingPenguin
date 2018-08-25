from flask import Blueprint
from flask_restplus import Api
from src.surfing_penguin import __version__
from src.surfing_penguin.extensions import flask_admin, session
from flask_admin.contrib.sqla import ModelView
from src.surfing_penguin.models import User

flask_admin.add_view(ModelView(User, session, endpoint="Users"))


api_prefix = "/api/"+__version__[0:3]
blueprint = Blueprint("api",
                      __name__,
                      url_prefix=api_prefix)

api = Api(blueprint,
          version=__version__[0:3],
          title="Surfing Penguin API",
          doc="/doc")

from src.surfing_penguin.API import user_api, survey_api  # noqa
