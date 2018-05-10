import os
import sys
from flask import Flask
import json
import pytest

parent_path = os.path.dirname(os.getcwd())
grand_parent_path = os.path.dirname(parent_path)

sys.path.append(grand_parent_path)

from src.config import TestConfig  # NOQA
from src.surfing_penguin.routes import blueprint  # NOQA
from src.surfing_penguin import create_login_manager  # NOQA


@pytest.fixture
def app():
    app = Flask(__name__)

    app.config.from_object(TestConfig)
    app.register_blueprint(blueprint)
    login_manager = create_login_manager(app)  # NOQA
    # TODO: create app by create_app()
    # TODO: check if using the correct database

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


# TODO: separate test functions to different classes


def test_hi(client):
    response = client.get('/api/hi')
    assert response.status_code == 200


def test_doc(client):
    response = client.get('/api/doc')
    assert response.status_code == 200


def test_register(client):
    test_data = {'username': 'c', 'password': 'b'}

    response = post_json(client,
                         '/api/register',
                          test_data)
    assert response.status_code == 200


# NOTE: this is just an example. This would not pass the pytest
# and should be under the same class with test_register()
def test_show_users(client):
    response = client.get('/api/show_users')
    assert 'a' in json_of_response(response)[0]['username']
    assert response.status_code == 200
