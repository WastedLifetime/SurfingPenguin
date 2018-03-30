"""routes.py: Each function in this file indicates a web page (HTML page)."""

from surfing_penguin import surfing_penguin, api
from flask import render_template, flash, redirect, url_for
from flask_restplus import Resource, fields
from surfing_penguin.forms import LoginForm
from surfing_penguin.db_interface import Qstnr, UserFunctions

question = api.model("question_model", {
        'content': fields.String,
        'id': fields.Integer
    })


api_user = api.model("user_model", {
        'username': fields.String,
        'id': fields.Integer,
        'password': fields.String,
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
    @api.marshal_with(api_user)
    @api.expect(api_user)
    def post(self):
        name = api.payload['username']
        password = api.payload['password']
        if UserFunctions.search_user(name) is True:
            return {'messages': "use another name"}
        return UserFunctions.register(name, password)


@api.route('/login')
class login(Resource):
    @api.marshal_with(api_user)
    @api.expect(api_user)
    def post(self):
        name = api.payload['username']
        password = api.payload['password']
        if UserFunctions.search_user(name) is False:
            return {'messages': "user not found"}
        if UserFunctions.check_password(name, password) is False:
            return {'messages': "wrong passwd"}
        return {'messages': "Login: {}".format(name)}


@api.route('/show_users')
class show_users(Resource):
    @api.marshal_list_with(api_show_user)
    def get(self):
        users = UserFunctions.get_all_users()
        return users


@api.route('/delete_user')
class delete_user(Resource):
    @api.marshal_with(api_user)
    @api.expect(api_user)
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
