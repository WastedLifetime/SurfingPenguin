import os
import sys
import pytest

parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)

from src.config import TestConfig  # NOQA
from src.surfing_penguin.routes import blueprint  # NOQA
from src.surfing_penguin import create_app  # NOQA


@pytest.fixture(scope='class')
def app():
    app = create_app(TestConfig)
    app.register_blueprint(blueprint)
    return app


@pytest.fixture(scope='class')
def session(app):
    from src.surfing_penguin.extensions import session
    from src.surfing_penguin.models import User
    new_user = User('admin', 'admin', 'admin')
    new_user.id = session.query(User).count() + 1
    session.add(new_user)
    session.commit()
    return session


@pytest.fixture
def client(app):
    test_client = app.test_client()

    def teardown():
        pass

    return test_client


@pytest.fixture
def api_prefix():
    from src.surfing_penguin import __version__
    ver = __version__[0:3]
    prefix = '/api/'+ver+'/'
    return prefix
