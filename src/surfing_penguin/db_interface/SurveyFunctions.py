from src.surfing_penguin.extensions import session
from src.surfing_penguin.models import Survey, Question


def new_survey(name, questions):
    survey = Survey(name)
    session.add(survey)
    session.commit()
    for i in range(len(questions)):
        new_question(survey, questions[i])
    return survey


def get_all_surveys():
    surveys = session.query(Survey).all()
    return surveys


def id_get_survey(ID):
    return session.query(Survey).filter_by(id=ID).first()


def name_get_survey(name):
    return session.query(Survey).filter_by(surveyname=name).first()


def new_question(survey, data):
    """
    Add a question to a survey

    Args:
        survey: survey object in ORM
        data: a dictionary with key "content" and "title"
    """
    survey.question_num += 1
    question = Question(data["title"], data["content"], survey)
    session.add(question)
    session.commit()
