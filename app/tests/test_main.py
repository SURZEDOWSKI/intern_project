from fastapi.testclient import TestClient
from app.main import app, create_users
import pytest


client = TestClient(app)


user1 = {
    "country": "PL",
    "dateOfBirth": "1999-08-06",
    "firstName": "Szymon",
    "lastName": "Urzedowski",
    "nickname": "Wazon",
    "gender": "male",
    "email": "wazon@gmail.com",
}


user2 = {
    "country": "PL",
    "dateOfBirth": "1990-08-06",
    "firstName": "Paweł",
    "lastName": "Nowak",
    "nickname": "Nowy",
    "gender": "male",
    "email": "nowy@gmail.com",
}


user3 = {
    "country": "PL",
    "dateOfBirth": "1995-08-06",
    "firstName": "Anna",
    "lastName": "Kowalska",
    "nickname": "Ania",
    "gender": "female",
    "email": "ania@gmail.com",
}


def create_users():
    client.post("/v1/users", json=user1)
    client.post("/v1/users", json=user2)
    client.post("/v1/users", json=user3)


create_users()


def test_get_user():
    response = client.get("/v1/users/1")
    assert response.status_code == 200
    out = {"id": 1}
    out.update(user1)
    assert response.json() == out


def test_get_user_out_of_index():
    response = client.get("/v1/users/5")
    assert response.status_code == 404


new_user = {
    "country": "NL",
    "dateOfBirth": "02.03.1992",
    "firstName": "Brian",
    "lastName": "Lemmen",
    "nickname": "Elmo",
    "gender": "male",
    "email": "elmo@gmail.com",
}


def test_create_user():
    response = client.post("/v1/users", json=new_user)
    assert response.status_code == 200
    out = {"id": 4}
    out.update(new_user)
    assert response.json() == out


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
    response = client.put("/v1/users", json=new_user)
    assert response.status_code == 405


def test_edit_user():
    response = client.put("/v1/users/1", json=new_user)
    assert response.status_code == 200
    out = {"id": 1}
    out.update(new_user)
    assert response.json() == out


def test_edit_user_out_of_index():
    response = client.put("/v1/users/6", json=new_user)
    assert response.status_code == 404


def test_edit_user_missing_query_argument():
    response = client.put(
        "/v1/users/4",
        json={
            "country": "string",
            "dateOfBirth": "string",
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
    ("user_id", "nickname", "email", "expected"),
    (
        (None, None, None, 200),
        ([1], None, None, 200),
        ([5], None, None, 404),
        ([1, 2, 3], None, None, 200),
        ([1, 2, 4], None, None, 200),
        ([4, 5], None, None, 404),
        (None, "A", None, 200),
        (None, "Pjoter", None, 404),
        (None, None, "a", 200),
        (None, None, "pjoter", 404),
        (None, "A", "a", 400),
        ([1, 2, 3], "A", None, 400),
    ),
)
def test_query_get_users(user_id, nickname, email, expected):

    query = ""
    if user_id != None:
        for i in range(len(user_id)):
            query = query + f"&user_id={user_id[i]}"
    if nickname != None:
        query = query + f"&nickname={nickname}"
    if email != None:
        query = query + f"&email={email}"

    response = client.get(f"/v1/users?{query}")
    assert response.status_code == expected
