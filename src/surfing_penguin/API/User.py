"""routes.py: Each function in this file indicates a web page (HTML page)."""
from src.surfing_penguin import surfing_penguin
from src.surfing_penguin.extensions import login_manager
from src.surfing_penguin.routes import api
from flask_restplus import Resource, fields
from src.surfing_penguin.db_interface import UserFunctions
from flask_login import login_user, logout_user, current_user, login_required


# TODO: separate expected and returned api models
# TODO: add help and others (like default) for each field
api_return_message = api.model("return_message_model", {
        'messages': fields.String(description="Messages returned")
    })

api_get_user = api.model("get_user_model", {
        'username': fields.String(description="Username"),
        'password': fields.String(description="Password(not encrypted)"),
    })

api_return_user = api.model("return_user_model", {
        'username': fields.String(description="Username"),
        'messages': fields.String(description="Messages returned"),
    })

api_show_user = api.model("show_user_model", {
        'username': fields.String(description="Username"),
    })

api_show_user_and_time = api.model("show_user_and_time_model", {
        'messages': fields.String(description="Messages returned"),
        'username': fields.String(description="Username"),
        'last_seen': fields.DateTime(
            description="Last time the user made a request")
    })


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
            return {'messages': "Hi, {}!".format(current_user.username)}
        return {'messages': "Hi, stranger!"}


@api.route('/register')
class register(Resource):
    @api.marshal_with(api_return_user)
    @api.expect(api_get_user)
    def post(self):
        name = api.payload['username']
        password = api.payload['password']
        if UserFunctions.get_user(name) is not None:
            return {'messages': "Use another name"}
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
        if UserFunctions.get_user(name) is None:
            return {'messages': "User not found"}
        if UserFunctions.check_password(name, password) is False:
            return {'messages': "Wrong passwd"}
        user = UserFunctions.get_user(name)
        login_user(user)
        return {'messages': "Login: {}".format(name)}


@api.route('/logout')
class logout(Resource):
    @api.marshal_with(api_return_message)
    def get(self):
        if current_user.is_authenticated:
            logout_user()
            return {'messages': "User logged out"}
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
            return {'messages': "User not found"}
        UserFunctions.delete_user(name)
        return {'messages': "User {} deleted".format(name)}


@api.route('/search_user')
class search_user(Resource):
    @api.marshal_with(api_show_user_and_time)
    @api.expect(api_show_user)
    def post(self):
        search_name = api.payload['username']
        if UserFunctions.get_user(search_name) is None:
            return {'messages': "user does not exist"}
        return UserFunctions.get_user(search_name)


@login_manager.unauthorized_handler
@api.marshal_with(api_return_message)
def unauthorized():
    # TODO: Flash this message somewhere.
    return {'messages': "Please Login First"}
