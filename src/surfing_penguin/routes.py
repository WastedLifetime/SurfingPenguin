"""routes.py: Each function in this file indicates a web page (HTML page)."""
from flask import Blueprint
from flask_restplus import Api
from src.surfing_penguin import surfing_penguin
from src.surfing_penguin.extensions import login_manager
from flask_restplus import Resource, fields
from src.surfing_penguin.db_interface import UserFunctions, SurveyFunctions
from flask_login import login_user, logout_user, current_user, login_required


blueprint = Blueprint("api",
                      __name__,
                      url_prefix="/api")

api = Api(blueprint,
          version="0.1",
          title="Surfing Penguin API",
          doc="/doc")

# TODO: separate expected and returned api models
# TODO: add help and others (like default) for each field
api_return_message = api.model("return_message_model", {
        'messages': fields.String,
    })

api_get_user = api.model("get_user_model", {
        'username': fields.String,
        'password': fields.String,
    })

api_return_user = api.model("return_user_model", {
        'username': fields.String,
        'messages': fields.String,
    })

api_show_user = api.model("show_user_model", {
        'username': fields.String,
    })

api_show_user_and_time = api.model("show_user_and_time_model", {
        'username': fields.String,
        'last_seen': fields.DateTime,
        'messages': fields.String,
    })

api_survey_name = api.model("survey_name", {
        'name': fields.String,
    })

api_survey_id = api.model("survey_id", {
        'id': fields.Integer,
    })

api_question = api.model("question_model", {
        'idx': fields.Integer,
        'title': fields.String,
        'content': fields.String,
    })

# TODO: add question_num and category (for meta class) in api_survey
api_survey = api.model("survey_model", {
        'id': fields.Integer,
        'surveyname': fields.String,
        'questions': fields.List(fields.Nested(api_question)),
    })

""" survey associated APIs """
# TODO: add error handling for functions that change the database
# (e.g., creating a survey with existing name)


@api.route('/create_survey')
class create_survey(Resource):
    @api.marshal_with(api_return_message)
    @api.expect(api_survey)
    def post(self):
        SurveyFunctions.new_survey(
                api.payload['surveyname'], api.payload['questions'])
        return {'messages': "survey created"}


@api.route('/show_all_surveys')
class show_surveys(Resource):
    @api.marshal_list_with(api_survey)
    def get(self):
        return SurveyFunctions.get_all_surveys()


@api.route('/search_survey_by_id')
class search_survey_by_id(Resource):
    """
    Show the information of a survey, given its name or ID.
    """
    @api.marshal_list_with(api_survey)
    @api.expect(api_survey_id)
    def post(self):
        return SurveyFunctions.id_get_survey(api.payload['id'])


@api.route('/search_survey_by_name')
class search_survey_by_name(Resource):
    """
    Show the information of a survey, given its name or ID.
    """
    @api.marshal_list_with(api_survey)
    @api.expect(api_survey_name)
    def post(self):
        return SurveyFunctions.name_get_survey(api.payload['name'])


""" user account associated APIs:
    register, login, show_users, delete_user, search_user """


@surfing_penguin.before_request
def before_request():
    # before each operation of a user, update his/her last_seen
    if current_user.is_authenticated:
        UserFunctions.update_last_seen(current_user.username)


@api.route('/hi')
class hi(Resource):
    @api.marshal_with(api_return_message)
    def get(self):
        if current_user.is_authenticated:
            return {'messages': "hi, {}!".format(current_user.username)}
        return {'messages': "hi, stranger!"}


@api.route('/register')
class register(Resource):
    @api.marshal_with(api_return_user)
    @api.expect(api_get_user)
    def post(self):
        name = api.payload['username']
        password = api.payload['password']
        if UserFunctions.search_user(name) is True:
            return {'messages': "use another name"}
        return UserFunctions.register(name, password)


@api.route('/login')
class login(Resource):
    @api.marshal_with(api_return_message)
    @api.expect(api_get_user)
    def post(self):
        if current_user.is_authenticated:
            return {'messages': "You had logged in before."}
        name = api.payload['username']
        password = api.payload['password']
        if UserFunctions.search_user(name) is False:
            return {'messages': "user not found"}
        if UserFunctions.check_password(name, password) is False:
            return {'messages': "wrong passwd"}
        user = UserFunctions.get_user(name)
        login_user(user)
        return {'messages': "Login: {}".format(name)}


@api.route('/logout')
class logout(Resource):
    @api.marshal_with(api_return_message)
    def get(self):
        if current_user.is_authenticated:
            logout_user()
            return {'messages': "user logged out"}
        return {'messages': "You did not logged in"}


@api.route('/show_users')
class show_users(Resource):
    @api.marshal_list_with(api_show_user)
    def get(self):
        users = UserFunctions.get_all_users()
        return users


@api.route('/delete_user')
class delete_user(Resource):
    @api.marshal_with(api_return_message)
    @api.expect(api_get_user)
    @login_required
    def post(self):
        name = api.payload['username']
        if UserFunctions.search_user(name) is False:
            return {'messages': "user not found"}
        UserFunctions.delete_user(name)
        return {'messages': "user {} deleted".format(name)}


@api.route('/search_user')
class search_user(Resource):
    @api.marshal_with(api_show_user_and_time)
    @api.expect(api_show_user)
    def post(self):
        search_name = api.payload['username']
        if UserFunctions.search_user(search_name) is False:
            return {'messages': "user does not exist"}
        return UserFunctions.get_user(search_name)


@login_manager.unauthorized_handler
@api.marshal_with(api_return_message)
def unauthorized():
    # TODO: Flash this message somewhere.
    print("entering")
    return {'messages': "Please Login First"}


def convert_user_to_json(user):
    json_user = {
        "username": user.username,
        "register_time": user.register_time.isoformat(),
        "last_login": user.last_login.isoformat()
    }
    return json_user


def convert_users_to_json(users):
    json_users = []
    for user in users:
        json_users.append(convert_user_to_json(user))
    return json_users
