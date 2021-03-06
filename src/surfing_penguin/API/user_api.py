from flask_restplus import Resource, fields
from functools import wraps
from flask_login import login_user, logout_user, current_user
from src.surfing_penguin import surfing_penguin
from src.surfing_penguin.routes import api
from src.surfing_penguin.extensions import login_manager
from src.surfing_penguin.db_interface import user_functions


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


def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return {'messages': "Please Login First"}

            if ((current_user.user_role not in role.split(',')) and
               (role != "ANY")):
                return {'messages': "You don't have permission!"}
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@surfing_penguin.before_request
def before_request():
    ''' Before each operation of a user, update his/her last_seen '''
    if current_user.is_authenticated:
        user_functions.update_last_seen(current_user.username)


@api.route('/hi')
class hi(Resource):
    ''' Check who is the current user'''
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
        try:
            name = api.payload['username']
            password = api.payload['password']
            if user_functions.get_user(name) is not None:
                return {'messages': "Use another name"}, 403
            return user_functions.register(name, password)
        except KeyError:
            return {'messages': "Invalid input format"}, 403


@api.route('/login')
class login(Resource):
    @api.marshal_with(api_return_message)
    @api.expect(api_get_user)
    def post(self):
        if current_user.is_authenticated:
            return {'messages': "You had logged in before."}, 403
        try:
            name = api.payload['username']
            password = api.payload['password']
            if user_functions.get_user(name) is None:
                return {'messages': "User not found"}, 403
            if user_functions.check_password(name, password) is False:
                return {'messages': "Wrong passwd"}, 403
            user = user_functions.get_user(name)
            login_user(user)
            return {'messages': "Login: {}".format(name)}
        except KeyError:
            return {'messages': "Invalid input format"}, 400


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
    ''' Show the list of all user'''
    @api.marshal_list_with(api_show_user)
    def get(self):
        users = user_functions.get_all_users()
        return users


@api.route('/delete_user')
class delete_user(Resource):
    @api.marshal_with(api_return_message)
    @api.expect(api_get_user)
    @login_required(role='ANY')
    def post(self):
        try:
            name = api.payload['username']
            if (current_user.user_role != 'admin' and
                    current_user.username != name):
                return {'messages': "You don't have permission!"}
            if user_functions.search_user(name) is False:
                return {'messages': "User not found"}
            user_functions.delete_user(name)
            return {'messages': "User {} deleted".format(name)}
        except KeyError:
            return {'messages': "Invalid input format"}, 400


@api.route('/search_user')
class search_user(Resource):
    @api.marshal_with(api_show_user_and_time)
    @api.expect(api_show_user)
    def post(self):
        try:
            search_name = api.payload['username']
            if user_functions.get_user(search_name) is None:
                return {'messages': "User not found"}
            return user_functions.get_user(search_name)
        except KeyError:
            return {'messages': "Invalid input format"}, 400


@login_manager.unauthorized_handler
@api.marshal_with(api_return_message)
def unauthorized():
    return {'messages': "Please Login First"}
