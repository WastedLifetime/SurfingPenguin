import os
import sys
import pytest
from utils import post_json, json_of_response

parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)

from src.surfing_penguin.models import Survey, Question, AnswerList, Answer # NOQA
import src.surfing_penguin.db_interface.SurveyFunctions as SurveyFunctions  # NOQA


@pytest.fixture
def survey():
    new_survey = Survey("test")
    return new_survey


# data for questions in survey
@pytest.fixture
def question_data():
    data = [
        {
            'idx': 1,
            'title': "testQ1",
            'content': "Q1content"
        },
        {
            'idx': 2,
            'title': "testQ2",
            'content': "Q2content"
            }
    ]
    return data


# data for a survey
@pytest.fixture
def survey_data(question_data):
    survey = {
        'id': 2,
        'surveyname': 'test_api',
        'questions': question_data
    }
    return survey


@pytest.fixture
def survey_with_question(question_data):
    # NOTE: This fixture should only be used
    # after TestSurvey class passes the tests.
    survey = SurveyFunctions.new_survey("survey_with_question", question_data)
    return survey


@pytest.fixture
def answer_data():
    data = [
        {
            'idx': 1,
            'content': "Ans1content"
        },
        {
            'idx': 2,
            'content': "Ans2content"
        }
    ]
    return data


@pytest.fixture
def answerlist_data(answer_data):
    anslist = {
        'survey_id': 2,
        'answers': answer_data
    }
    return anslist


@pytest.mark.usefixtures('session')
class TestSurvey():

    # NOTE: Test functions in this class use the same database.

    """ Testing models """
    def test_survey_model(self, survey):
        assert(survey.surveyname == "test")
        assert(survey.question_num == 0)
        assert(survey.answerlist_num == 0)

    def test_question_model(self, survey):
        question = Question("TITLE", "CONTENT", survey)
        assert(question.title == "TITLE")
        assert(question.content == "CONTENT")
        assert(question.survey_id == survey.id)
        assert(question.idx == survey.question_num)

    """ Testing db operations """
    def test_new_survey(self, session, question_data):
        test_survey = SurveyFunctions.new_survey("test", question_data)
        assert(test_survey.surveyname == "test")
        assert(test_survey.question_num == len(question_data))
        assert(session.query(Question).filter_by(
            survey_id=test_survey.id).count() == len(question_data))

    def test_get_all_surveys(self):
        surveys = SurveyFunctions.get_all_surveys()
        assert (surveys[0].surveyname == "test")

    def test_id_get_survey(self):
        survey = SurveyFunctions.id_get_survey(1)
        assert (survey.surveyname == "test")

    def test_name_get_survey(self):
        survey = SurveyFunctions.name_get_survey("test")
        assert (survey.question_num == 2)

    # NOTE: Function new_question() is not tested,
    # because it's called in new_survey() in db_operation.

    """ Testing api """
    def test_create_survey(self, survey_data, client, api_prefix):
        url = api_prefix+'create_survey'
        response = post_json(client, url, survey_data)
        assert (response.status_code == 200)
        assert (json_of_response(response)['messages'] == "Survey created")

    def test_new_survey_bad_request(self, client, api_prefix):
        url = api_prefix+'create_survey'
        response = post_json(client, url, {})
        assert (response.status_code == 400)
        assert (json_of_response(response)['messages'] ==
                "Invalid input format")
        response = post_json(client, url, {'surveyname': None})
        assert (response.status_code == 400)
        assert (json_of_response(response)['messages'] ==
                "Invalid input: No survey name")
        response = post_json(client, url, {'surveyname': "test_api"})
        assert (response.status_code == 200)
        assert (json_of_response(response)['messages'] ==
                "The name of the survey had been used")

    def test_show_all_surveys(self, client, api_prefix):
        url = api_prefix+'show_all_surveys'
        response = client.get(url)
        assert response.status_code == 200
        assert json_of_response(response)[0]['surveyname'] == "test"

    def test_search_survey_by_id(self, client, api_prefix):
        url = api_prefix+'search_survey_by_id'
        response = post_json(client, url, {'id': 1})
        assert response.status_code == 200
        assert json_of_response(response)['surveyname'] == "test"

    def test_search_survey_by_name(self, client, api_prefix):
        url = api_prefix+'search_survey_by_name'
        response = post_json(client, url, {'name': "test"})
        assert response.status_code == 200
        assert json_of_response(response)['id'] == 1


@pytest.mark.usefixtures('session')
class TestAnswer():

    """ Testing models """
    def test_answerlist_model(self, survey):
        test_answerlist = AnswerList(survey)
        assert test_answerlist.survey_id == survey.id
        assert test_answerlist.idx == survey.answerlist_num

    def test_answer_model(self, session, survey_with_question):
        test_answerlist = AnswerList(survey_with_question)
        target_question = session.query(Question).filter_by(
            survey_id=survey_with_question.id).first()
        test_answer = Answer(test_answerlist, target_question, "answer:123")
        assert test_answer.answerlist_id == test_answerlist.id
        assert test_answer.idx == target_question.idx
        assert test_answer.question_id == target_question.id
        assert test_answer.content == "answer:123"

    """ Testing db operations """
    def test_new_answerlist(
            self, session, answerlist_data, survey_with_question):
        answerlist = SurveyFunctions.new_answerlist(answerlist_data)
        assert answerlist.survey_id == answerlist_data['survey_id']
        assert session.query(AnswerList).filter_by(
                survey_id=answerlist_data['survey_id']).first() is not None

    def test_id_get_answerlist_num(self):
        num = SurveyFunctions.id_get_answerlist_num(2)
        assert num == 1

    def test_id_get_answerlists(self):
        lists = SurveyFunctions.id_get_answerlists(2)
        assert lists[0].answers[0].idx == 1
        assert lists[0].answers[0].content == "Ans1content"

    # NOTE: Function new_answer() is not tested,
    # because it's called in new_answerlist() in db_operation.

    """ Testing api """
    def test_answer_a_survey(
            self, client, api_prefix, answerlist_data):
        url = api_prefix+'answer_a_survey'
        response = post_json(client, url, answerlist_data)
        assert response.status_code == 200
        assert json_of_response(response)['messages'] == "Answer completed"

    def test_answer_a_survey_bad_request(self, client, api_prefix):
        url = api_prefix+'answer_a_survey'
        response = post_json(client, url, {})
        assert response.status_code == 400
        assert json_of_response(response)['messages'] == "Invalid input format"
        response = post_json(client, url, {'survey_id': 100})
        assert response.status_code == 400
        assert json_of_response(response)['messages'] == "Survey not found"

    def test_show_answers(
            self, session, client, api_prefix,):
        url = api_prefix+'show_answers'
        response = post_json(client, url, {"id": 2})
        assert response.status_code == 200
        assert json_of_response(response)['survey_id'] == 2
        assert json_of_response(response)['answerlist_num'] == 2
        assert json_of_response(response)['answerlists'][0]['answers'][0] == {
                    'idx': 1,
                    'content': "Ans1content"
                }

    def test_show_answers_bad_request(self, client, api_prefix):
        url = api_prefix+'show_answers'
        response = post_json(client, url, {})
        assert response.status_code == 400
        assert json_of_response(response)['messages'] == "Invalid input format"
        response = post_json(client, url, {"id": 100})
        assert response.status_code == 400
        assert json_of_response(response)['messages'] == "Survey not found"
