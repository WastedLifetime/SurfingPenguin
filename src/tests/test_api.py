import os
import sys
import json
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


# TODO: separate test functions to different classes


def test_hi(client):
    response = client.get('/api/hi')
    assert json_of_response(response)['messages'] == "hi, stranger!"
    assert response.status_code == 200


def test_doc(client):
    response = client.get('/api/doc')
    assert response.status_code == 200
