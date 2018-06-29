import os
import sys
import pytest
from utils import post_json, json_of_response

parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)

from src.surfing_penguin.models import Survey, Question # NOQA
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


@pytest.mark.usefixtures('session')
class TestSurvey():

    # NOTE: Test functions in this class use the same database.

    """ Testing models """
    def test_survey_model(self, survey):
        assert(survey.surveyname == "test")
        assert(survey.question_num == 0)

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
