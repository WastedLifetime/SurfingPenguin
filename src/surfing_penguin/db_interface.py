import datetime
from src.surfing_penguin import session, login_manager
from src.surfing_penguin.models import User, Survey, Question


class UserFunctions(object):
    def search_user(name):
        if session.query(User).filter_by(username=name).first() is not None:
            return True
        return False

    def get_user(name):
        return session.query(User).filter_by(username=name).first()

    def register(name, password):
        if session.query(User).filter_by(username=name).first() is not None:
            return
        new_user = User(name, password)
        new_user.id = session.query(User).count() + 1
        session.add(new_user)
        session.commit()
        return new_user

    def check_password(name, password):
        user = session.query(User).filter_by(username=name).first()
        return user.check_password(password)

    def get_all_users():
        users = session.query(User).all()
        return users

    def delete_user(name):
        session.query(User).filter_by(username=name).delete()
        session.commit()

    def update_last_seen(name):
        user = session.query(User).filter_by(username=name).first()
        user.last_seen = datetime.datetime.utcnow()
        session.commit()


@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))


class SurveyFunctions(object):
    def __init__(self, name):
        self.iter = 0
        self.name = name
        survey = Survey(name)
        session.add(survey)
        session.commit()

    def get_all_surveys():
        surveys = session.query(Survey).all()
        return surveys

    def get_all_questions(name):
        s = session.query(Survey).filter_by(surveyname=name).first()
        return s.questions

    def new_question(self, data):
        # data should be a dictionary, with key "content" and "title"
        question = Question()
        question.title = data["title"]
        question.content = data["content"]
        self.iter = self.iter + 1
        question.idx = self.iter
        s = session.query(Survey).filter_by(surveyname=self.name).first()
        question.survey_id = s.id
        session.add(question)
        session.commit()
        return question
