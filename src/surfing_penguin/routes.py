"""routes.py: Each function in this file indicates a web page (HTML page)."""

from surfing_penguin import surfing_penguin, api, auth
from flask import request, g, render_template, flash, redirect, url_for
from flask_restplus import Resource, fields
from surfing_penguin.forms import LoginForm
from surfing_penguin.db_interface import Qstnr, UserFunctions
from surfing_penguin.models import User
from functools import wraps

api_return_message = api.model("return_message", {
        'message': fields.String
    })


api_token = api.model("api_token", {
        'token': fields.String,
        'duration': fields.Integer
    })


question = api.model("question_model", {
        'content': fields.String,
        'id': fields.Integer
    })


api_get_user = api.model("get_user_model", {
        'username': fields.String,
        'password': fields.String,
    })


api_return_user = api.model("return_user_model", {
        'username': fields.String,
        'id': fields.Integer,
        'messages': fields.String,
    })


api_show_user = api.model("show_user_model", {
        'username': fields.String,
        'id': fields.Integer,
    })


qstnrs = [
    {
        'author': {'username': 'John'},
        'title': 'QSTQ',
        'id': 0
    },
    {
        'author': {'username': 'Susan'},
        'title': 'QSTQQ',
        'id': 1
    }
]
qstnr1 = Qstnr()
qstnr1.new_qst({'content': 'Q1'})
qstnr1.new_qst({'content': 'Q2'})


# TODO:combine it with HTTPauth
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {'message': 'Token is missing.'}, 401

        if token != 'mytoken':
            return {'message': 'Your token is wrong, wrong, wrong!!!'}, 401

        return f(*args, **kwargs)

    return decorated


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = UserFunctions.get_user(username_or_token)
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@api.route('/api_token')
class api_token(Resource):
    @auth.login_required
    @api.marshal_with(api_token)
    def get(self):
        token = g.user.generate_auth_token(600)
        return {'token': token.decode('ascii'), 'duration': 600}


@api.route('/api_resource')
class api_resource(Resource):
    @auth.login_required
    @api.marshal_with(api_return_message)
    def get(self):
        return {'message': 'hi, user {}'.format(g.user.username)}


@api.route('/api_display')
class api_display(Resource):
    """ This api is for developers to monitor the program,
        currently only showing the questionnaire.
        usage: start the server, and curl localhost:port/api_display """
    @api.marshal_list_with(question)
    def get(self):
        return qstnr1.questions


""" user account associated APIs:
    register, login, show_users, delete_user, search_user """


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


# TODO: combine this with HTTPauth
@api.route('/login')
class login(Resource):
    @api.marshal_with(api_return_user)
    @api.expect(api_get_user)
    def post(self):
        name = api.payload['username']
        password = api.payload['password']
        if UserFunctions.search_user(name) is False:
            return {'messages': "user not found"}
        user = UserFunctions.get_user(name)
        if user.verify_password(password) is False:
            return {'messages': "wrong passwd"}
        return {'username': name, 'messages': "Login: {}".format(name)}


@api.route('/logout')
class logout(Resource):
    @api.marshal_with(api_return_message)
    def get(self):
        return {'message': 'user logout'}


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
    # @api.doc(security='apikey')
    # @token_required
    @auth.login_required
    def post(self):
        name = api.payload['username']
        if UserFunctions.search_user(name) is False:
            return {'messages': "user not found"}
        UserFunctions.delete_user(name)
        return {'messages': "user {} deleted".format(name)}


@api.route('/search_user')
class search_user(Resource):
    @api.marshal_with(api_show_user)
    @api.expect(api_show_user)
    def post(self):
        search_name = api.payload['username']
        if UserFunctions.search_user(search_name) is False:
            return {'messages': "user does not exist"}
        return UserFunctions.get_user(search_name)


@api.route('/show_surveys')
class show_surveys(Resource):
    def get(self):
        return qstnrs


@api.route('/fill/<int:qstnr_id>')
class fill(Resource):
    def get(self, qstnr_id):
        return qstnrs[qstnr_id]


@surfing_penguin.route('/index')
def index():
    return render_template('index.html')


@surfing_penguin.route('/login_html', methods=['GET', 'POST'])
def login_html():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@surfing_penguin.route('/select_qstnr')
def select_qstnr():
    """Show the list of questionnaires.
       Clients should pick up one and go to filling_in."""
    return render_template('select_qstnr.html', qstnrs=qstnrs)


@surfing_penguin.route('/filling_in')
def filling_in():
    qstnr = [
        {
            'question': 'test Q1'
        },
        {
            'question': 'test Q2'
        }
    ]
    return render_template('filling_in.html', qstnr=qstnr)


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
