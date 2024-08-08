from fastapi.testclient import TestClient
from fastapi import status
from fastapi_app.main import app
from unittest.mock import MagicMock, patch
import pytest
from fastapi_app.src.database.models import User, Photo
from fastapi_app.src.services.auth import auth_service
from fastapi_app.src.services.auth import Auth

client = TestClient(app=app)

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


def test_create__test_photo_authorized(client, token):
    """
    Creation photo to testing"""
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

def test_create_test_comment_for_photo(client, token):
    """Creation comment for testing"""
    response = client.post(
        "/api/comments/photos/1/comments/",
        json={"content": "I like it"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["content"] == "I like it"
    assert "id" in data

def test_read_photo_authorized_by_rating(client, token):
    """
    Test about reading photo by photo descriptions and rating
    """
    response = client.get('http://localhost:8000/api/search_filter/photos/search/garden?rating_filter=0')
    headers={"Authorization": f"Bearer {token}"}
    assert response.status_code == 200, response.text

def test_read_photo_authorized_by_creation_date(client, token):
    """
    Test about reading photo by photo descriptions and creation date
    """
    response = client.get('http://localhost:8000/api/search_filter/photos/search/garden?created_at=2024-07-29')
    headers={"Authorization": f"Bearer {token}"}
    assert response.status_code == 200, response.text

def test_read_photo_authorized_by_tag_and_rating(client, token):
    """
    Test about reading photo by tag and rating
    """
    response = client.get('http://localhost:8000/api/search_filter/photos/search/tag/pretty?rating_filter=0')
    headers={"Authorization": f"Bearer {token}"}
    assert response.status_code == 200, response.text

def test_read_photo_authorized_by_tag_and_created_date(client, token):
    """
    Test about reading photo by tag and photo created date
    """
    response = client.get('http://localhost:8000/api/search_filter/photos/search/tag/pretty?created_at=2024-07-29')
    headers={"Authorization": f"Bearer {token}"}
    assert response.status_code == 200, response.text