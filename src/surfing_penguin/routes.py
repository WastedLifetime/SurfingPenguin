"""routes.py: Each function in this file indicates a web page (HTML page)."""

from surfing_penguin import surfing_penguin, api
from flask import render_template, flash, redirect, url_for, request
from flask_restplus import Resource, fields
from surfing_penguin.forms import LoginForm
from surfing_penguin.db_interface import Qstnr

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


@api.route('/api_login')
class api_login(Resource):
    def get(self):
        return "Please Login"

    def post(self):
        user = request.form['user']
        password = request.form['passwd']
        return "Login: %s, %s" % (user, password)


@api.route('/show_surveys')
class show_surveys(Resource):
    def get(self):
        return qstnrs


@api.route('/fill/<int:qstnr_id>')
class fill(Resource):
    def get(self, qstnr_id):
        return qstnrs[qstnr_id]


@surfing_penguin.route('/')
@surfing_penguin.route('/index')
def index():
    return render_template('index.html')


@surfing_penguin.route('/login', methods=['GET', 'POST'])
def login():
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
