from fastapi.testclient import TestClient
from ..main import app, usr_create
import pytest
import json

client = TestClient(app)


def test_get_user():
    response = client.get("/v1/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "country": "PL",
        "dateOfBirth": "1999-08-06",
        "firstName": "Szymon",
        "lastName": "Urzedowski",
        "nickname": "Wazon",
        "gender": "male",
        "email": "wazon@gmail.com",
    }


def test_get_user_out_of_index():
    response = client.get("/v1/users/5")
    assert response.status_code != 200


def test_create_user():
    response = client.post(
        "/v1/users",
        json={
            "country": "NL",
            "dateOfBirth": "02.03.1992",
            "firstName": "Brian",
            "lastName": "Lemmen",
            "nickname": "Elmo",
            "gender": "male",
            "email": "elmo@gmail.com",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 4,
        "country": "NL",
        "dateOfBirth": "02.03.1992",
        "firstName": "Brian",
        "lastName": "Lemmen",
        "nickname": "Elmo",
        "gender": "male",
        "email": "elmo@gmail.com",
    }


def test_create_user_missing_argument():
    response = client.post(
        "/v1/users",
        json={
            "country": "string",
            "dateOfBirth": "string",
            "firstName": "string",
            "lastName": "string",
        },
    )
    assert response.status_code == 422


def test_create_user_wrong_method():
    response = client.put(
        "/v1/users",
        json={
            "country": "string",
            "dateOfBirth": "string",
            "firstName": "string",
            "lastName": "string",
            "nickname": "string",
            "gender": "string",
            "email": "string",
        },
    )
    assert response.status_code == 405


def test_edit_user():
    response = client.put(
        "/v1/users/1",
        json={
            "country": "UK",
            "dateOfBirth": "19.09.1980",
            "firstName": "Adam",
            "lastName": "Smith",
            "nickname": "Adi",
            "gender": "male",
            "email": "adi@gmail.com",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "country": "UK",
        "dateOfBirth": "19.09.1980",
        "firstName": "Adam",
        "lastName": "Smith",
        "nickname": "Adi",
        "gender": "male",
        "email": "adi@gmail.com",
    }


def test_edit_user_out_of_index():
    response = client.put(
        "/v1/users/6",
        json={
            "country": "string",
            "dateOfBirth": "string",
            "firstName": "string",
            "lastName": "string",
            "nickname": "string",
            "gender": "string",
            "email": "string",
        },
    )
    assert response.status_code == 404


def test_edit_user_missing_query_argument():
    response = client.put(
        "/v1/users/5",
        json={
            "country": "string",
            "dateOfBirth": "string",
            "firstName": "string",
            "lastName": "string",
        },
    )
    assert response.status_code == 422


def test_delete_user():
    response = client.delete("/v1/users/4")
    assert response.status_code == 200


def test_delete_user_out_of_index():
    response = client.delete("/v1/users/6")
    assert response.status_code == 404


def test_delete_user_missing_index():
    response = client.delete("/v1/users")
    assert response.status_code == 405


@pytest.mark.parametrize(
    ("path", "expected"),
    (
        ("/v1/users", 200),
        ("/v1/users?user_id=1", 200),
        ("/v1/users?user_id=5", 404),
        ("/v1/users?user_id=1&user_id=2&user_id=3", 200),
        ("/v1/users?user_id=1&user_id=2&user_id=4", 200),
        ("/v1/users?user_id=4&user_id=5&user_id=6", 404),
        ("/v1/users?nickname=A", 200),
        ("/v1/users?nickname=Pioter", 404),
        ("/v1/users?email=a", 200),
        ("/v1/users?email=pioter", 404),
        ("/v1/users?nickname=A&email=a", 400),
    ),
)
def test_query_get_users(path, expected):
    response = client.get(path)
    assert response.status_code == expected
