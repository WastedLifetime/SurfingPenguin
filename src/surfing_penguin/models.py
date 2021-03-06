""" models.py: Classes that tell the content in the database."""

import datetime
from src.surfing_penguin.extensions import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
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
    survey = relationship("Survey")

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


class Survey(Base):
    __tablename__ = 'survey'
    id = Column(Integer, primary_key=True)
    survey_title = Column(String(128))
    survey_content = Column(String(128))  # Briefly describe it
    question_num = Column(Integer)
    is_anonymous = Column(Integer, default=0)
    answerlist_num = Column(Integer)
    author_id = Column(Integer, ForeignKey('user.id'))
    questions = relationship("Question")
    answerlists = relationship("AnswerList")

    def __init__(self, user, name, content, is_anonymous):
        self.survey_title = name
        self.author_id = user.id
        self.survey_content = content
        self.question_num = 0
        self.answerlist_num = 0
        self.is_anonymous = is_anonymous


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    index_in_survey = Column(Integer)  # NO. in that survey
    title = Column(String(128))
    content = Column(String(1024))
    format = Column(Enum("Multiple-choice", "Short answer", name="format_enum",
                         create_type=False))
    choice_num = Column(Integer)
    survey_id = Column(Integer, ForeignKey('survey.id'))

    def __init__(self, title, content, format, choice_num, survey):
        self.title = title
        self.content = content
        self.format = format
        self.choice_num = choice_num
        self.survey_id = survey.id
        self.index_in_survey = survey.question_num


class AnswerList(Base):
    __tablename__ = 'answerlist'
    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('survey.id'))
    nickname = Column(String(128))
    answeruser_id = Column(Integer, ForeignKey('user.id'))
    index_in_survey = Column(Integer)
    answers = relationship("Answer")

    def __init__(self, user, survey, nickname):
        self.survey_id = survey.id
        self.index_in_survey = survey.answerlist_num
        self.answeruser_id = user.id
        self.nickname = nickname


class Answer(Base):
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True)
    answerlist_id = Column(Integer, ForeignKey('answerlist.id'))
    question_id = Column(Integer, ForeignKey('question.id'))
    question_index = Column(Integer, ForeignKey('question.index_in_survey'))
    content_string = Column(String(1024))
    question = relationship("Question", foreign_keys=[question_index])

    def __init__(self, answerlist, question, content_string):
        self.answerlist_id = answerlist.id
        self.question_index = question.index_in_survey
        self.question_id = question.id
        self.content_string = content_string
