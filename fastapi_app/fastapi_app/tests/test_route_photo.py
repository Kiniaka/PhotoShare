from fastapi.testclient import TestClient
from fastapi import status
from fastapi_app.main import app
from unittest.mock import MagicMock, patch
import pytest
from fastapi_app.src.database.models import User, Photo
from fastapi_app.src.services.auth import auth_service
from fastapi_app.src.services.auth import Auth


client = TestClient(app=app)

def test_create_photo_unauthorized():
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
  "rating": 0
})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

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

def test_read_photo_authorized(client, token):
    """
    Test about reading photo by id
    """
    response = client.get('http://localhost:8000/api/photos/photos/1')
    headers={"Authorization": f"Bearer {token}"}
    assert response.status_code == 200, response.text

def test_update_photo_authorized(client, token):
    """
    Test about updating photo's description by photo id
    """
    response = client.put('http://localhost:8000/api/photos/photos/1?description=grass')
    headers={"Authorization": f"Bearer {token}"}
    assert response.status_code == 200, response.text

def test_delete_photo_authorized(client, token):
    """
    Test about deleting photo by photo id
    """
    response = client.delete('http://localhost:8000/api/photos/photos/1')
    headers={"Authorization": f"Bearer {token}"}
    assert response.status_code == 200, response.text

def test_delete_photo_not_found():
    """
    Test about deleting photo by photo id
    """
    response = client.delete('http://localhost:8000/api/photos/photos/3')
    assert response.status_code == 404, response.text