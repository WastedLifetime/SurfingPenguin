from src.surfing_penguin.extensions import session
from src.surfing_penguin.models import Survey, Question, AnswerList, Answer


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
    Add a question to a survey, temporarily only called by new_survey

    Args:
        survey: survey object in ORM
        data: a dictionary with key "content" and "title"
    """
    survey.question_num += 1
    question = Question(data["title"], data["content"], survey)
    session.add(question)
    session.commit()


def new_answerlist(data):
    """
    Answerlist is a data structure that stores
    a list of answers of a specified survey.

    This function should create a new answerlist and all answers in it.

    Args:
        data: a dictionary with key "survey_id" and a list of
                answers(which is a dictionary with key 'idx and 'content'')
    """
    survey = session.query(Survey).filter_by(id=data["survey_id"]).first()
    survey.answerlist_num += 1
    answerlist = AnswerList(survey)
    session.add(answerlist)
    session.commit()
    for i in range(len(data["answers"])):
        question = session.query(Question).filter_by(
                survey_id=survey.id, idx=i+1).first()
        new_answer(answerlist, question, data["answers"][i])
    return answerlist


def new_answer(answerlist, question, data):
    """
    Add a new answer to a question, only called by new_answerlist
    """
    answer = Answer(answerlist, question, data["content"])
    session.add(answer)
    session.commit()


def id_get_answerlist_num(ID):
    return session.query(AnswerList).filter_by(survey_id=ID).count()


def id_get_answerlists(ID):
    return session.query(AnswerList).filter_by(survey_id=ID).all()
