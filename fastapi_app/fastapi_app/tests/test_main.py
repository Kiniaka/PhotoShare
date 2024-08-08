from fastapi.testclient import TestClient
from fastapi import status
from fastapi_app.main import app

client = TestClient(app=app)

def test_return_corrent_main():
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World"}