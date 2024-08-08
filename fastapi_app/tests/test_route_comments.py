from fastapi.testclient import TestClient
from fastapi import status
from fastapi_app.main import app

from unittest.mock import MagicMock, patch

import pytest

from fastapi_app.src.database.models import User, Photo
from fastapi_app.src.services.auth import auth_service

client = TestClient(app=app)

def test_create_photo_authorized(client, token):
    """
    Test with confirme that the photo can't be found and it doen not exist. 
    The reason it that the creation photo could not be able  is because there is no user who is loggin so can't created photo"""
    response = client.post("http://localhost:8000/api/photos/photos/?description=garden&tags=pretty", json={
  "url": "uploads/e9571dba-5f2c-4760-ad54-be4a93389665.jpeg",
  "user_id": 1,
  "id": 3,
  "description": "garden",
  "created_at": "2024-07-28T22:40:48.533017",
  "updated_at": "null",
  "rating": 0}, headers={"Authorization": f"Bearer {token}"}, files = {"file": "@Woda.jpeg;type=image/jpeg"} )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["description"] == "garden"
    assert "id" in data


def test_create_comment_for_photo_unauthorized():
    """
    Test with confirme that the commend to photo with ID nr equil 3 can't be found and it doen not exist. 
    The reason it that the creation comment could not be able  is because there is no user who is loggin so can't created comment
    """
    response = client.post("http://localhost:8000/api/comments/photos/3/comments/", json={
        "content": "I really like it",
        "id": 3,
        "created_at": "2024-07-28T22:41:58.181172",
        "updated_at": "2024-07-28T22:41:58.181172",
        "user_id": 1,
        "photo_id": 3
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# def test_create_comment_for_photo_authorized():
#     """
#     Test with confirme that the commend to photo with ID nr equil 3 can't be found and it doen not exist. 
#     The reason it that the creation comment could not be able  is because there is no user who is loggin so can't created comment
#     """

#     response = client.post("http://localhost:8000/api/comments/photos/1/comments/", json={
#         "content": "I really like it",
#         "id": 1,
#         "created_at": "2024-07-28T22:41:58.181172",
#         "updated_at": "2024-07-28T22:41:58.181172",
#         "user_id": 1,
#         "photo_id": 1
#     })
#     assert response.status_code == status.HTTP_200_OK

def test_return_status_create_comment():
    """Checking if the url to created comment to photo with is = 1 exist when comment with ID nr 1 exist in db"""
    response = client.get("http://localhost:8000/docs#/comments/photos/1/comments/")
    assert response.status_code == status.HTTP_200_OK


def test_return_status_update_comment():
    """checking if url to update comment for photo exist"""
    response = client.get("http://localhost:8000/docs#/comments/update_comment_api_comments_comments_comment_id_put")
    assert response.status_code == status.HTTP_200_OK

@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("fastapi_app.src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('username'), "password": user.get('password')}
    )
    data = response.json()
    return data["access_token"]

def test_create_comment_for_photo(client, token):
    response = client.post(
        "/api/comments/photos/1/comments/",
        json={"content": "I like it"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["content"] == "I like it"
    assert "id" in data

def test_update_comment_for_photo(client, token):
    response = client.post(
        "http://localhost:8000/api/comments/photos/1/comments/",
        json={"content": "I like it"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["content"] == "I like it"
    assert "id" in data

def test_read_comment_for_photo(client, token):
    response = client.get(
        "http://localhost:8000/api/comments/comments/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["content"] == "I like it"
    assert "id" in data

def test_read_comment_for_photo(client, token):
    response = client.get(
        "http://localhost:8000/api/comments/comments/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["content"] != "Great"
    assert "id" in data

def test_delete_comment_for_photo(client, token):
    response = client.delete(
        "http://localhost:8000/api/comments/comments/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
