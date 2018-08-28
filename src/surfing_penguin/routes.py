from flask import Blueprint
from flask_restplus import Api
from src.surfing_penguin import __version__
from src.surfing_penguin.models import User
from src.surfing_penguin.view import view
from src.surfing_penguin.extensions import flask_admin, session


flask_admin.add_view(view.Admin_View(User, session, endpoint="Users"))
# flask_admin should add in extensions but it doesn't work

api_prefix = "/api/"+__version__[0:3]
blueprint = Blueprint("api",
                      __name__,
                      url_prefix=api_prefix)

api = Api(blueprint,
          version=__version__[0:3],
          title="Surfing Penguin API",
          doc="/doc")

from src.surfing_penguin.API import user_api, survey_api  # noqa
