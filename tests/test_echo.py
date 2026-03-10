import requests
import pytest

url_get = "https://postman-echo.com/get" 
url_post = "https://postman-echo.com/post"

@pytest.fixture
def create_user():
    user_data = {"name": "Sofa", "age": "25"}
    post_response = requests.post(f"{url_post}", json=user_data)
    assert post_response.status_code == 200
    user = post_response.json()
    yield user
    requests.delete(f"{url_post}")

def test_get_request_params(create_user): 
    user = create_user
    params = {
        "gender": "M"
    }
    response = requests.get(f"{url_get}", params=params)
    assert response.status_code == 400
    data = response.json()
    assert data["args"]["gender"] == "M"

def test_post_form_d(create_user): 
    user = create_user
    form_data = {
        "name": "Peter", 
        "age": "18",
        "gender": "M"
    }
    response = requests.post(f"{url_post}", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert data["form"]["name"] == "Peter"
    assert data["form"]["age"] == "18"
    assert data["form"]["gender"] == "M"

def test_none_id(): 
    response = requests.get(f"{url_get}/users/none_id")
    assert response.status_code == 404

def test_get_none_param(create_user): 
    user = create_user
    params = {
        "family": "",
        "city": None
    }
    response = requests.get(f"{url_get}", params=params)
    assert response.status_code == 200
    data = response.json()
    assert "family" in data["args"]

def test_post_user(): 
    user = {"name": "Ivan", "family": "Petrov"}
    response = requests.post(f"{url_post}", json=user)
    assert response.status_code == 200
    user_req = response.json()
    assert user["name"] == "Ivan"
    assert user["family"] == "Petrov"
