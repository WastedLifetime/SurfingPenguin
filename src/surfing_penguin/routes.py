from flask import Blueprint
from flask_restplus import Api
from flask_login import current_user
from src.surfing_penguin import __version__
from src.surfing_penguin.extensions import flask_admin, session
from flask_admin.contrib.sqla import ModelView
from src.surfing_penguin.models import User


class View(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and (
                                            current_user.user_role == 'admin')


flask_admin.add_view(View(User, session, endpoint="Users"))


api_prefix = "/api/"+__version__[0:3]
blueprint = Blueprint("api",
                      __name__,
                      url_prefix=api_prefix)

api = Api(blueprint,
          version=__version__[0:3],
          title="Surfing Penguin API",
          doc="/doc")

from src.surfing_penguin.API import user_api, survey_api  # noqa
