import os
import sys
import pytest
from utils import post_json, json_of_response

parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)


@pytest.fixture(scope="function")
def login_as_c(client, api_prefix):
    test_data = {'username': 'c', 'password': 'b'}
    post_json(client, api_prefix+'register', test_data)
    post_json(client, api_prefix+'login', test_data)
    return


@pytest.fixture(scope="function")
def login_as_admin(client, api_prefix):
    test_data = {'username': 'admin', 'password': 'admin'}
    post_json(client, api_prefix+'register', test_data)
    post_json(client, api_prefix+'login', test_data)
    return


def test_hi(client, api_prefix):
    url = api_prefix+'hi'
    response = client.get(url)
    assert json_of_response(response)['messages'] == "Hi, stranger!"
    assert response.status_code == 200


def test_doc(client, api_prefix):
    url = api_prefix+'doc'
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.usefixtures('session', 'client')
class TestRegister():

    def test_register(self, client, api_prefix):
        test_data = {'username': 'c', 'password': 'b'}
        url = api_prefix+'register'
        response = post_json(client, url, test_data)
        assert json_of_response(response)['username'] == "c"
        assert response.status_code == 200

    def test_register_with_the_same_name(self, client, api_prefix):
        test_data = {'username': 'c', 'password': 'b'}
        url = api_prefix+'register'
        response = post_json(client, url, test_data)
        assert json_of_response(response)['messages'] == "Use another name"
        assert response.status_code == 403

    def test_register_bad_request(self, client, api_prefix):
        url = api_prefix+'register'
        response = post_json(client, url, {})
        assert response.status_code == 403
        assert json_of_response(response)['messages'] == "Invalid input format"

    def test_show_users(self, client, api_prefix):
        url = api_prefix+'show_users'
        response = client.get(url)
        assert json_of_response(response)[1]['username'] == "c"
        assert response.status_code == 200

    def test_search_user(self, client, api_prefix):
        test_data = {'username': 'c'}
        url = api_prefix+'search_user'
        response = post_json(client, url, test_data)
        assert json_of_response(response)['username'] == "c"
        assert json_of_response(response)['last_seen'] is not None
        assert response.status_code == 200

    def test_search_user_with_not_found(self, client, api_prefix):
        test_data = {'username': 'd'}
        url = api_prefix+'search_user'
        response = post_json(client, url, test_data)
        assert json_of_response(response)['messages'] == "User not found"
        assert response.status_code == 200

    def test_search_user_bad_request(self, client, api_prefix):
        url = api_prefix+'search_user'
        response = post_json(client, url, {})
        assert response.status_code == 400
        assert json_of_response(response)['messages'] == "Invalid input format"

    def test_login_with_wrong_name(self, client, api_prefix):
        test_data = {'username': 'd', 'password': 'b'}
        url = api_prefix+'login'
        response = post_json(client, url, test_data)
        assert json_of_response(response)['messages'] == "User not found"
        assert response.status_code == 403

    def test_login_with_wrong_pwd(self, client, api_prefix):
        test_data = {'username': 'c', 'password': 'c'}
        url = api_prefix+'login'
        response = post_json(client, url, test_data)
        assert json_of_response(response)['messages'] == "Wrong passwd"
        assert response.status_code == 403

    def test_login(self, client, api_prefix):
        test_data = {'username': 'c', 'password': 'b'}
        url = api_prefix+'login'
        response = post_json(client, url, test_data)
        assert json_of_response(response)['messages'] == "Login: c"
        assert response.status_code == 200

    def test_login_again(self, client, login_as_c, api_prefix):
        test_data = {'username': 'c', 'password': 'b'}
        url = api_prefix+'login'
        response = post_json(client, url,  test_data)
        assert json_of_response(response)['messages'] == \
            "You had logged in before."
        assert response.status_code == 403

    def test_login_bad_request(self, client, api_prefix):
        url = api_prefix+'login'
        response = post_json(client, url, {})
        assert json_of_response(response)['messages'] == "Invalid input format"
        assert response.status_code == 400

    def test_hi_c(self, client, login_as_c, api_prefix):
        url = api_prefix+'hi'
        response = client.get(url)
        assert json_of_response(response)['messages'] == "Hi, c!"
        assert response.status_code == 200

    def test_logout_without_login(self, client, api_prefix):
        url = api_prefix+'logout'
        response = client.get(url)
        assert json_of_response(response)['messages'] == \
            "You did not logged in"
        assert response.status_code == 200

    def test_logout(self, client, login_as_c, api_prefix):
        url = api_prefix+'logout'
        response = client.get(url)
        assert json_of_response(response)['messages'] == "User logged out"
        assert response.status_code == 200
        response = client.get(api_prefix+'logout')  # check for log out.
        assert json_of_response(response)['messages'] == \
            "You did not logged in"
        assert response.status_code == 200

    def test_delete_other_user(self, client, login_as_c, api_prefix):
        test_data = {'username': 'd'}
        url = api_prefix+'delete_user'
        response = post_json(client, url, test_data)
        assert json_of_response(response)['messages'] == \
            "You don't have permission!"
        assert response.status_code == 200

    def test_delete_user_not_found(self, client, login_as_admin, api_prefix):
        test_data = {'username': 'd'}
        url = api_prefix+'delete_user'
        response = post_json(client, url, test_data)
        assert json_of_response(response)['messages'] == "User not found"
        assert response.status_code == 200

    def test_delete_user_not_login(self, client, api_prefix):
        test_data = {'username': 'd'}
        url = api_prefix+'delete_user'
        response = post_json(client, url, test_data)
        assert json_of_response(response)['messages'] == "Please Login First"
        assert response.status_code == 200

    def test_delete_user_bad_request(self, client, login_as_c, api_prefix):
        url = api_prefix+'delete_user'
        response = post_json(client, url, {})
        assert json_of_response(response)['messages'] == "Invalid input format"
        assert response.status_code == 400

    def test_delete_user(self, client, login_as_c, api_prefix):
        test_data = {'username': 'c'}
        url = api_prefix+'delete_user'
        response = post_json(client, url, test_data)
        assert json_of_response(response)['messages'] == "User c deleted"
        assert response.status_code == 200
