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
    def new_survey(name, questions):
        survey = Survey(name)
        session.add(survey)
        session.commit()
        for i in range(len(questions)):
            SurveyFunctions.new_question(survey, questions[i])
        return survey

    def get_all_surveys():
        surveys = session.query(Survey).all()
        return surveys

    def get_survey(name, ID):
        """
        Return a specified survey, with priority: ID > name
        """
        if ID:
            survey = session.query(Survey).filter_by(id=ID).first()
            if survey:
                return survey
        return session.query(Survey).filter_by(surveyname=name).first()

    def new_question(survey, data):
        """
        Add a question to a survey

        arg:
            survey: survey object in ORM
            data: a dictionary with key "content" and "title"
        """
        survey.question_num += 1
        question = Question(data["title"], data["content"], survey)
        session.add(question)
        session.add(survey)
        session.commit()
