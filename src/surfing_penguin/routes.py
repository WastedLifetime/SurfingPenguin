"""routes.py: Each function in this file indicates a web page (HTML page)."""

import datetime
from surfing_penguin import surfing_penguin, api, session
from flask import render_template, flash, redirect, url_for, request
from flask_restplus import Resource, fields
from surfing_penguin.forms import LoginForm
from surfing_penguin.db_interface import Qstnr
from surfing_penguin.models import User

question = api.model("question_model", {
        'content': fields.String,
        'id': fields.Integer
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
    def get(self):
        return "register: enter username and password"

    def post(self):
        new_name = request.form['username']
        new_password = request.form['password']
        if session.query(User).filter_by(username=new_name).count() == 1:
            return "Please use another username"
        new_user = User(new_name, new_password)
        session.add(new_user)
        session.commit()
        return "registration done for user %s" % (new_user.username)


@api.route('/login')
class login(Resource):
    def get(self):
        return "login: enter username and password"

    def post(self):
        login_name = request.form['username']
        login_passwd = request.form['password']
        if session.query(User).filter_by(username=login_name).count() == 0:
            return "user not found"
        login_user = session.query(User).filter_by(username=login_name).first()
        if login_user.password != login_passwd:
            return "wrong password"
        login_user.last_login = datetime.datetime.utcnow()
        session.commit()
        return "Login: %s" % (login_user.username)


@api.route('/show_users')
class show_users(Resource):
    def get(self):
        return convert_users_to_json(session.query(User).all())


@api.route('/delete_user')
class delete_user(Resource):
    def get(self):
        return "delete_user: enter username"

    def post(self):
        delete_name = request.form['username']
        if session.query(User).filter_by(username=delete_name).count() == 0:
            return "user does not exist"
        session.query(User).filter_by(username=delete_name).delete()
        session.commit()
        return "user %s deleted" % (delete_name)


@api.route('/search_user')
class search_user(Resource):
    def get(self):
        return "search_user: enter username"

    def post(self):
        search_name = request.form['username']
        if session.query(User).filter_by(username=search_name).count() == 0:
            return "user does not exist"
        user = session.query(User).filter_by(username=search_name).first()
        return "user %s, register time: %s, last login: %s" % (
                user.username, user.register_time, user.last_login)


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
