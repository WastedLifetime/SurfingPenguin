import os
import sys
import json
import pytest

parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)

from src.config import TestConfig  # NOQA
from src.surfing_penguin.routes import blueprint  # NOQA
from src.surfing_penguin import create_app  # NOQA
from src.surfing_penguin.models import Survey, Question # NOQA
import src.surfing_penguin.db_interface.SurveyFunctions as SurveyFunctions  # NOQA


@pytest.fixture(scope='class')
def app():
    app = create_app(TestConfig)
    app.register_blueprint(blueprint)
    # TODO: check if using the correct database
    return app


@pytest.fixture(scope='class')
def session(app):
    from src.surfing_penguin.extensions import session
    return session


@pytest.fixture
def client(app):
    test_client = app.test_client()

    def teardown():
        pass
        # Databases and resourses have to be freed at
        # the end.

    # request.addfinalizer(teardown)
    return test_client


@pytest.fixture
def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict),
                       content_type='application/json')


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


# TODO: separate test functions to different classes
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


@pytest.mark.usefixtures('session')
class TestSurvey():
    # Warning: Test functions in this class
    # use the same database, so be mindful of the
    # sequece to call them.

    """ testing models """
    def test_Survey_model(self, survey):
        assert(survey.surveyname == "test")
        assert(survey.question_num == 0)

    def test_Question_model(self, survey):
        question = Question("TITLE", "CONTENT", survey)
        assert(question.title == "TITLE")
        assert(question.content == "CONTENT")
        assert(question.survey_id == survey.id)
        assert(question.idx == survey.question_num)

    # testing db operations

    def test_new_survey(self, session, question_data):
        test_survey = SurveyFunctions.new_survey("test", question_data)
        assert(test_survey.surveyname == "test")
        assert(test_survey.question_num == 2)
        assert(session.query(Question).filter_by(
            survey_id=test_survey.id).count() == 2)

    def test_get_all_surveys(self):
        surveys = SurveyFunctions.get_all_surveys()
        assert (surveys[0].surveyname == "test")

    def test_id_get_survey(self):
        survey = SurveyFunctions.id_get_survey(1)
        assert (survey.surveyname == "test")

    def test_name_get_survey(self):
        survey = SurveyFunctions.name_get_survey("test")
        assert (survey.question_num == 2)

    # new_question function not tested

    # testing api
    def test_create_survey(self, question_data, client):
        survey = {
            'id': 2,
            'surveyname': 'test_api',
            'questions': question_data
        }
        url = '/api/create_survey'
        response = post_json(client, url, survey)
        assert (response.status_code == 200)
        assert (json_of_response(response)['messages'] == "survey created")

    def test_show_all_surveys(self, client):
        response = client.get('/api/show_all_surveys')
        assert response.status_code == 200
        assert json_of_response(response)[0]['surveyname'] == "test"

    def test_search_survey_by_id(self, client):
        url = '/api/search_survey_by_id'
        response = post_json(client, url, {'id': 1})
        assert response.status_code == 200
        assert json_of_response(response)['surveyname'] == "test"

    def test_search_survey_by_name(self, client):
        url = '/api/search_survey_by_name'
        response = post_json(client, url, {'name': "test"})
        assert response.status_code == 200
        assert json_of_response(response)['id'] == 1
