""" models.py: Classes that tell the content in the database."""

from surfing_penguin import db, api
from flask_restplus import fields


question = api.model("question_model", {
        'content': fields.String,
        'id': fields.Integer
    })


class Qstnr(object):
    def __init__(self):
        self.iter = 0
        self.questions = []

    def get(self, id):
        for qst in self.questions:
            if qst['id'] == id:
                return qst
        api.abort(404, "question {} doesn't exist".format(id))

    def new_qst(self, data):
        question = data
        self.iter = self.iter + 1
        question['id'] = self.iter
        self.questions.append(question)
        return question

    def delete(self, id):
        question = self.get(id)
        self.question.remove(question)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
