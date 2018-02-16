from surfing_penguin import surfing_penguin
from flask import render_template, flash, redirect
from surfing_penguin.forms import LoginForm

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
    qstnrs = [
        {
            'author': {'username': 'John'},
            'title': 'QSTQ'
        },
        {
            'author': {'username': 'Susan'},
            'title': 'QSTQQ'
        }
    ]
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

