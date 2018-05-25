import os
import sys
import json
import datetime
import pytest

parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)

from src.config import TestConfig  # NOQA
from src.surfing_penguin.routes import blueprint  # NOQA
from src.surfing_penguin import create_app  # NOQA


@pytest.fixture
def app():
    app = create_app(TestConfig)
    from src.surfing_penguin import extensions
    extensions.init_app(app)
    app.register_blueprint(blueprint)

    return app


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


def test_doc(client):
    response = client.get('/api/doc')
    assert response.status_code == 200

# TODO: separate test functions to different classes


def test_hi(client):
    response = client.get('/api/hi')
    assert json_of_response(response)['messages'] == "hi, stranger!"
    assert response.status_code == 200


def test_doc(client):
    response = client.get('/api/doc')
    assert response.status_code == 200

class TestRegister():

    def test_register(self, client):
        test_data = {'username': 'c', 'password': 'b'}
        response = post_json(client, '/api/register', test_data)
        assert json_of_response(response)['username'] == "c"
        assert response.status_code == 200

    def test_show_users(self, client):
        response = client.get('/api/show_users')
        assert json_of_response(response)[0]['username'] == "c"
        assert response.status_code == 200

    def test_search_user(self, client):
        test_data = {'username': 'c'}
        response = post_json(client, '/api/search_user', test_data)
        assert json_of_response(response)['username'] == "c"
        assert json_of_response(response)['last_seen'] is not None
<<<<<<< HEAD
        assert response.status_code == 200

    def test_login_with_wrong_name(self, client):
        test_data = {'username': 'd', 'password': 'b'}
        response = post_json(client, '/api/login', test_data)
        assert json_of_response(response)['messages'] == "user not found"
        assert response.status_code == 200

    def test_login_with_wrong_pwd(self, client):
        test_data = {'username': 'c', 'password': 'c'}
        response = post_json(client, '/api/login', test_data)
        assert json_of_response(response)['messages'] == "wrong passwd"
        assert response.status_code == 200

    def test_login(self, client):
        test_data = {'username': 'c', 'password': 'b'}
        response = post_json(client, '/api/login', test_data)
        assert json_of_response(response)['messages'] == "Login: c"
        assert response.status_code == 200

    def test_login_again(self, client):
        test_data = {'username': 'c', 'password': 'b'}
        response = post_json(client, '/api/login', test_data)
        assert json_of_response(response)['messages'] == "You had logged in before."
        assert response.status_code == 200

    def test_login_with_wrong_name(self, client):
        test_data = {'username': 'd', 'password': 'b'}
        response = post_json(client, '/api/login', test_data)
        assert json_of_response(response)['messages'] == "user not found"
        assert response.status_code == 200

    def test_login_with_wrong_pwd(self, client):
        test_data = {'username': 'c', 'password': 'c'}
        response = post_json(client, '/api/login', test_data)
        assert json_of_response(response)['messages'] == "wrong passwd"
        assert response.status_code == 200

    def test_login(self, client):
        test_data = {'username': 'c', 'password': 'b'}
        response = post_json(client, '/api/login', test_data)
        assert json_of_response(response)['messages'] == "Login: c"
        assert response.status_code == 200

    def test_login_again(self, client):
        test_data = {'username': 'c', 'password': 'b'}
        response = post_json(client, '/api/login', test_data)
        assert json_of_response(response)['messages'] == "You had logged in before."
        assert response.status_code == 200
        
