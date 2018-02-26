"""routes.py: Each function in this file indicates a web page (HTML page)."""

from surfing_penguin import api
from flask import request
from flask_restplus import Resource


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


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/index')
class index(Resource):
    def get(self):
        return "Welcome to Surfing Penguin"


@api.route('/login')
class login(Resource):
    def get(self):
        return "Please Login"

    def post(self):
        user = request.form['user']
        password = request.form['passwd']
        return "Login: %s, %s" % (user, password)


@api.route('/select')
class select(Resource):
    def get(self):
        return qstnrs


@api.route('/fill/<int:qstnr_id>')
class fill(Resource):
    def get(self, qstnr_id):
        return qstnrs[qstnr_id]
