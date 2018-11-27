import os
import sys
import pytest
from utils import post_json, json_of_response

parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)

from src.surfing_penguin.models import Survey, Question, AnswerList, Answer, User # NOQA
from src.surfing_penguin.db_interface import survey_functions  # NOQA


@pytest.fixture
def login_as_c(client, api_prefix):
    test_data = {'username': 'c', 'password': 'b'}
    post_json(client, api_prefix+'register', test_data)
    post_json(client, api_prefix+'login', test_data)
    return


@pytest.fixture
def survey():
    new_user = User("test", "testpwd", "normal")
    new_user.id = 1
    new_survey = Survey(new_user, "test", 0)
    return new_survey


# data for questions in survey
@pytest.fixture
def question_data():
    data = [
        {
            'index_in_survey': 1,
            'title': "testQ1",
            'content': "Q1content"
        },
        {
            'index_in_survey': 2,
            'title': "testQ2",
            'content': "Q2content"
            }
    ]
    return data


# data for a survey
@pytest.fixture
def survey_data(question_data):
    survey = {
        'survey_title': 'test_api',
        'questions': question_data,
        'is_anonymous': 0
    }
    return survey


@pytest.fixture
def survey_with_question(question_data):
    # NOTE: This fixture should only be used
    # after TestSurvey class passes the tests.
    new_user = User("test", "testpwd", "normal")
    new_user.id = 1
    survey = survey_functions.new_survey(new_user, "survey_with_question",
                                         question_data, 0)
    return survey


@pytest.fixture
def answer_data():
    data = [
        {
            'index_in_survey': 1,
            'content': "Ans1content"
        },
        {
            'index_in_survey': 2,
            'content': "Ans2content"
        }
    ]
    return data


@pytest.fixture
def answerlist_data(answer_data):
    anslist = {
        'survey_id': 2,
        'answers': answer_data,
        'answeruser_id': 1,
        'nickname': "client"
    }
    return anslist


@pytest.mark.usefixtures('session')
class TestSurvey():

    # NOTE: Test functions in this class use the same database.

    """ Testing models """
    def test_survey_model(self, survey):
        assert(survey.survey_title == "test")
        assert(survey.question_num == 0)
        assert(survey.answerlist_num == 0)

    def test_question_model(self, survey):
        question = Question("TITLE", "CONTENT", survey)
        assert(question.title == "TITLE")
        assert(question.content == "CONTENT")
        assert(question.survey_id == survey.id)
        assert(question.index_in_survey == survey.question_num)

    """ Testing db operations """
    def test_new_survey(self, session, question_data):
        new_user = User("test", "testpwd", "normal")
        new_user.id = 1
        test_survey = survey_functions.new_survey(new_user, "test",
                                                  question_data, 0)
        assert(test_survey.survey_title == "test")
        assert(test_survey.question_num == len(question_data))
        assert(session.query(Question).filter_by(
            survey_id=test_survey.id).count() == len(question_data))

    def test_get_all_surveys(self):
        surveys = survey_functions.get_all_surveys()
        assert (surveys[0].survey_title == "test")

    def test_id_get_survey(self):
        survey = survey_functions.id_get_survey(1)
        assert (survey.survey_title == "test")

    def test_name_get_survey(self):
        survey = survey_functions.name_get_surveys("test")
        assert (survey[0].survey_title == "test")

    # NOTE: Function new_question() is not tested,
    # because it's called in new_survey() in db_operation.

    """ Testing api """
    def test_create_survey(self, survey_data, login_as_c, client, api_prefix):
        url = api_prefix+'create_survey'
        response = post_json(client, url, survey_data)
        assert (response.status_code == 200)
        assert (json_of_response(response)['messages'] == "Survey created")

    def test_new_survey_bad_request(self, client, login_as_c, api_prefix):
        url = api_prefix+'create_survey'
        response = post_json(client, url, {})
        assert (response.status_code == 400)
        assert (json_of_response(response)['messages'] ==
                "Invalid input format")
        response = post_json(client, url, {'survey_title': None})
        assert (response.status_code == 400)
        assert (json_of_response(response)['messages'] ==
                "Invalid input: No survey name")

    def test_show_all_surveys(self, client, api_prefix):
        url = api_prefix+'show_all_surveys'
        response = client.get(url)
        assert response.status_code == 200
        assert json_of_response(response)[0]['survey_title'] == "test"

    def test_search_survey_by_id(self, client, api_prefix):
        url = api_prefix+'search_survey_by_id'
        response = post_json(client, url, {'id': 1})
        assert response.status_code == 200
        assert json_of_response(response)['survey_title'] == "test"

    def test_search_survey_by_name(self, client, api_prefix):
        url = api_prefix+'search_survey_by_name'
        response = post_json(client, url, {'name': "test"})
        assert response.status_code == 200
        assert json_of_response(response)[0]['id'] == 1


@pytest.mark.usefixtures('session')
class TestAnswer():

    """ Testing models """
    def test_answerlist_model(self, survey):
        new_user = User("test", "testpwd", "normal")
        test_answerlist = AnswerList(new_user, survey, "client")
        assert test_answerlist.survey_id == survey.id
        assert test_answerlist.index_in_survey == survey.answerlist_num

    def test_answer_model(self, session, survey_with_question):
        new_user = User("test", "testpwd", "normal")
        test_answerlist = AnswerList(new_user, survey_with_question, "client")
        target_question = session.query(Question).filter_by(
            survey_id=survey_with_question.id).first()
        test_answer = Answer(test_answerlist, target_question, "answer:123")
        assert test_answer.answerlist_id == test_answerlist.id
        assert test_answer.question_index == target_question.index_in_survey
        assert test_answer.question_id == target_question.id
        assert test_answer.content == "answer:123"

    """ Testing db operations """
    def test_new_answerlist(
            self, session, answerlist_data, survey_with_question):
        new_user = User("test", "testpwd", "normal")
        answerlist = survey_functions.new_answerlist(new_user, answerlist_data)
        assert answerlist.survey_id == answerlist_data['survey_id']
        assert session.query(AnswerList).filter_by(
                survey_id=answerlist_data['survey_id']).first() is not None

    def test_id_get_answerlist_num(self):
        num = survey_functions.id_get_answerlist_num(2)
        assert num == 1

    def test_id_get_answerlists(self):
        lists = survey_functions.id_get_answerlists(2)
        assert lists[0].answers[0].question_index == 1
        assert lists[0].answers[0].content == "Ans1content"

    # NOTE: Function new_answer() is not tested,
    # because it's called in new_answerlist() in db_operation.

    """ Testing api """
    def test_answer_a_survey(
            self, client, api_prefix, login_as_c, answerlist_data):
        url = api_prefix+'answer_a_survey'
        response = post_json(client, url, answerlist_data)
        assert response.status_code == 200
        assert json_of_response(response)['messages'] == "Answer completed"

    def test_answer_a_survey_bad_request(self, client, login_as_c, api_prefix):
        url = api_prefix+'answer_a_survey'
        response = post_json(client, url, {})
        assert response.status_code == 400
        assert json_of_response(response)['messages'] == "Invalid input format"
        response = post_json(client, url, {'survey_id': 100})
        assert response.status_code == 400
        assert json_of_response(response)['messages'] == "Survey not found"
        data = [
            {
                'index_in_survey': 5,
                'content': "Ans1content"
            },
            {
                'index_in_survey': 3,
                'content': "Ans2content"
            }
        ]
        response = post_json(client, url, {
                'survey_id': 2,
                'answers': data,
                'answeruser_id': 1,
                'nickname': "client"
                })
        assert response.status_code == 400
        assert json_of_response(response)['messages'] == "Question not found"

    def test_show_answers(
            self, session, client, api_prefix,):
        url = api_prefix+'show_answers'
        response = post_json(client, url, {"id": 2})
        assert response.status_code == 200
        assert json_of_response(response)['survey_id'] == 2
        assert json_of_response(response)['answerlist_num'] == 2
        assert json_of_response(response)['answerlists'][0]['answers'][0] == {
                    'question_index': 1,
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
