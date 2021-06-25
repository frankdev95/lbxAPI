from starlette.testclient import TestClient
from main import app
from utils.db_functions import get_insert_query, get_fetch_query, get_delete_query
from utils.db import execute, fetch
from utils.test_records import user, post_user
import asyncio

client = TestClient(app)
loop = asyncio.get_event_loop()


def get_auth_header():
    insert_user()
    response = client.post("/token", dict(username="test", password="test123"))
    jwt_token = response.json()["access_token"]

    return {"Authorization": f"Bearer {jwt_token}"}


def test_token_success():
    insert_user()
    response = client.post("/token", dict(username="test", password="test123"))

    assert response.status_code == 200
    assert "access_token" in response.json()

    clear_user_table()


def test_token_unauthorized():
    insert_user()
    response = client.post("/token", dict(username="test", password="test12"))

    assert response.status_code == 401

    clear_user_table()


def test_register_user():
    response = client.post("/signup", json=post_user)

    assert response.status_code == 201
    assert "token" in response.json()
    assert "user" in response.json()

    clear_user_table()


def test_post_user():
    response = client.post("/user", json=post_user, headers=get_auth_header())
    assert response.status_code == 201
    assert check_user(post_user["username"], post_user["email_address"]) == True

    clear_user_table()


def test_get_users():
    response = client.get("/users", headers=get_auth_header())
    assert response.status_code == 200

    clear_user_table()


def test_get_user_by_username():
    response = client.get("/user/test", headers=get_auth_header())
    assert response.status_code == 200
    assert "user" in response.json()

    clear_user_table()


def check_user(username, email_address):
    values = {
        "username": username,
        "email_address": email_address
    }

    query = get_fetch_query("users", "*", values)

    result = loop.run_until_complete(fetch(query, False, values))

    if result is None:
        return False

    return True


def insert_user():
    values = {**user}

    query = get_insert_query("users", values)

    loop.run_until_complete(execute(query, False, values))


def clear_user_table():
    delete_users = "DELETE FROM users"
    loop.run_until_complete(execute(delete_users, False))
    restart_sequence("users_id_seq")


def restart_sequence(sequence):
    query = f"ALTER SEQUENCE {sequence} RESTART 1"
    loop.run_until_complete(execute(query, False))