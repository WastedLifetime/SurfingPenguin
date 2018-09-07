""" models.py: Classes that tell the content in the database."""

import datetime
from src.surfing_penguin.extensions import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# TODO: separate models.py into serveral models

class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password_hash = Column(String(128))
    user_role = Column(String(32), default='normal')
    register_time = Column(DateTime, default=datetime.datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, password, user_role):
        self.username = username
        self.user_role = user_role
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return "User('{}', registered at '{}',last login:'{}')".format(
                self.username,
                self.register_time,
                self.last_seen
                )

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# A survey should include: title, author, time,
#   prize, description, type, num of answers
class Survey(Base):
    __tablename__ = 'survey'
    id = Column(Integer, primary_key=True)
    surveyname = Column(String(128))

    # TODO: connect author with user
    author = Column(String(128))

    prize_description = Column(String(128))
    survey_description = Column(String(1024))
    survey_type = Column(String(128))
    create_time = Column(DateTime, default=datetime.datetime.utcnow)

    # TODO: add bidirectional relastionship with question
    question_num = Column(Integer)
    answerlist_num = Column(Integer)
    questions = relationship("Question")
    answerlists = relationship("AnswerList")

    def __init__(self, data, author):
        self.surveyname = data['surveyname']
        self.author = author
        self.survey_description = data['survey_description']
        self.prize_description = data['prize_description']
        self.question_num = 0
        self.answerlist_num = 0


class Question(Base):
    # TODO: add detail in what should in a question
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    content = Column(String(1024))
    survey_id = Column(Integer, ForeignKey('survey.id'))
    idx = Column(Integer)  # NO. in that survey
    answers = relationship("Answer")
    # TODO: add answer type

    def __init__(self, title, content, survey):
        self.title = title
        self.content = content
        self.survey_id = survey.id
        self.idx = survey.question_num


class AnswerList(Base):
    """
    AnswerList is a table connecting Survey and Answer,
    where an Answer is an answer to only a question.
    """
    __tablename__ = 'answerlist'
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('survey.id'))
    idx = Column(Integer)  # No. in list of answerlist to that survey
    answers = relationship("Answer")
    # TODO: add author

    def __init__(self, survey):
        self.survey_id = survey.id
        self.idx = survey.answerlist_num


class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    answerlist_id = Column(Integer, ForeignKey('answerlist.id'))
    question_id = Column(Integer, ForeignKey('question.id'))
    idx = Column(Integer)  # NO. in that answerlist
    # TODO: add multiple answer type
    content = Column(String(1024))

    def __init__(self, answerlist, question, content):
        self.answerlist_id = answerlist.id
        self.idx = question.idx
        self.question_id = question.id
        self.content = content
