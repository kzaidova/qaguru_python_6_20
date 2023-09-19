import requests
import json
from jsonschema.validators import validate
from conftest import resources_path
import os



def test_all_users_schema():
    with open(os.path.join(resources_path, 'get_users_schema.json')) as file:
        schema = json.loads(file.read())

    response = requests.get("https://reqres.in/api/users")

    validate(instance=response.json(), schema=schema)


def test_single_users_schema():
    with open(os.path.join(resources_path, 'get_single_user_schema.json')) as file:
        schema = json.loads(file.read())

    response = requests.get("https://reqres.in/api/users/2")

    validate(instance=response.json(), schema=schema)


def test_get_all_users_list_is_200():
    resp = requests.get("https://reqres.in/api/users")
    print(resp.status_code)

    assert resp.status_code == 200


def test_users_per_page():
    per_page = 1

    response = requests.get(
        url="https://reqres.in/api/users",
        params={"per_page": per_page}
    )

    assert response.status_code == 200
    assert response.json()['per_page'] == per_page


def test_open_single_user_by_id():
    id = 5

    response = requests.get(
        url=f"https://reqres.in/api/users/{id}",
        params={"id": id}
    )

    assert response.status_code == 200
    assert response.json()['data']['id'] == id

def test_open_single_user_by_not_exist_id():
    id = 100

    response = requests.get(
        url=f"https://reqres.in/api/users/{id}",
        params={"id": id}
    )

    assert response.status_code == 404


def test_create_user():
    name = "Kate"
    job = "QA"

    response = requests.post(
        url='https://reqres.in/api/users',
        data={"name": name, "job": job}
    )

    assert response.status_code == 201
    assert response.json()['name'] == name
    assert response.json()['job'] == job


def test_user_register_successful():
    email = "eve.holt@reqres.in"
    password = "pistol"

    response = requests.post(
        url='https://reqres.in/api/register',
        data={"email": email, "password": password}
    )

    assert response.status_code == 200


def test_user_register_not_successful():
    password = "pistol"

    response = requests.post(
        url='https://reqres.in/api/register',
        data={"password": password}
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing email or username'


def test_login_not_successful():
    email = "eve.holt@reqres.in"
    password = "pistol"

    response = requests.post(
        url='https://reqres.in/api/register',
        data={email: email, "password": password}
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing email or username'


def test_login_successful():
    email = "eve.holt@reqres.in"
    password = "cityslicka"

    response = requests.post(
        url='https://reqres.in/api/login',
        data={"email": email, "password": password}
    )

    assert response.status_code == 200
