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
    def new_survey(name):
        survey = Survey(name)
        session.add(survey)
        session.commit()
        return survey

    def get_all_surveys():
        surveys = session.query(Survey).all()
        return surveys

    def get_all_questions(name):
        s = session.query(Survey).filter_by(surveyname=name).first()
        return s.questions

    def new_question(survey, data):
        # data should be a dictionary, with key "content" and "title"
        question = Question()
        question.title = data["title"]
        question.content = data["content"]
        survey.question_num += 1
        question.idx = survey.question_num
        question.survey_id = survey.id
        session.add(question)
        session.add(survey)
        session.commit()
