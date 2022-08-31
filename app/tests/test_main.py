from fastapi.testclient import TestClient
from ..main import app, usr_create

client = TestClient(app)

"""usr_create("PL", "1999-08-06", "Szymon", "Urzedowski", "Wazon", "male", "wazon@gmail.com")
usr_create("PL", "1990-08-06", "Paweł", "Nowak", "Nowy", "male", "nowy@gmail.com")
usr_create("PL", "1995-08-06", "Anna", "Kowalska", "Ania", "female", "ania@gmail.com")
"""

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
                                "email": "wazon@gmail.com"
                                 }


def test_get_user_out_of_index():
    response = client.get("/v1/users/5")
    assert response.status_code != 200


def test_create_user():
    response = client.post(
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
    assert response.status_code == 200
    assert response.json() == {
        "id": 4,
        "country": "string",
        "dateOfBirth": "string",
        "firstName": "string",
        "lastName": "string",
        "nickname": "string",
        "gender": "string",
        "email": "string",
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
    response = client.put("/v1/users/1", json={
            "country": "string",
            "dateOfBirth": "string",
            "firstName": "string",
            "lastName": "string",
            "nickname": "string",
            "gender": "string",
            "email": "string",
        },)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "country": "string",
        "dateOfBirth": "string",
        "firstName": "string",
        "lastName": "string",
        "nickname": "string",
        "gender": "string",
        "email": "string",
    }
    

def test_edit_user_out_of_index():
    response = client.put("/v1/users/6", json={
            "country": "string",
            "dateOfBirth": "string",
            "firstName": "string",
            "lastName": "string",
            "nickname": "string",
            "gender": "string",
            "email": "string",
        },)
    assert response.status_code == 404


def test_edit_user_missing_query_argument():
    response = client.put("/v1/users/5", json={
            "country": "string",
            "dateOfBirth": "string",
            "firstName": "string",
            "lastName": "string",
        },)
    assert response.status_code == 422


def test_delete_user():
    response = client.delete("/v1/users/1")
    assert response.status_code == 200


def test_delete_user_out_of_index():
    response = client.delete("/v1/users/6")
    assert response.status_code == 404


def test_delete_user_missing_index():
    response = client.delete("/v1/users")
    assert response.status_code == 405


def test_qeury_get_all_users():
    response = client.get("/v1/users")
    assert response.status_code == 200


def test_query_get_users_too_many_params():
    response = client.get("/v1/users?nickname=aaa&email=bbb")
    assert response.status_code == 400


### stąd jest źle
########### can't find user that is created first: 404
def test_query_get_users_by_id():
    response = client.get("/v1/users?user_id=1")
    assert response.status_code == 200

"""
def test_query_get_users_by_multiple_ids():
    response = client.get("/v1/users?user_id=1&user_id=2&user_id=3")
    assert response.status_code == 200


def test_query_get_users_by_multiple_ids_one_out_of_index():
    response = client.get("/v1/users?user_id=1&user_id=2&user_id=3&user_id=4")
    assert response.status_code == 200

def test_query_get_users_by_multiple_ids_all_out_of_index():
    response = client.get("/v1/users?user_id=4&user_id=5")
    assert response.status_code == 404

############# nie znajduje 1 usera
def test_query_get_users_by_nickname():
    response = client.get("/v1/users?nickname=A")
    assert response.status_code == 200"""