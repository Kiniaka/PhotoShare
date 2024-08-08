import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status

from fastapi_app.src.services.auth import Auth
from fastapi_app.src.database.models import User

class User:
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role


class MockSettings:
    secret_key = "test_secret"
    algorithm = "HS256"


class MockOAuth2PasswordBearer:
    tokenUrl = "/api/auth/login"


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_auth():
    return Auth()


@pytest.fixture
def mock_redis():
    redis_mock = MagicMock()

    redis_mock.get.return_value = '{"id": 1, "email": "test@example.com", "role": "user"}'
    redis_mock.set.return_value = None

    return redis_mock


@pytest.mark.asyncio
async def test_create_access_token(mock_auth, mock_db, mock_redis):
    mock_auth.SECRET_KEY = "test_secret"
    mock_auth.ALGORITHM = "HS256"
    data = {"sub": "test@example.com"}
    expires_delta = 3600

    token = await mock_auth.create_access_token(data, expires_delta)

    assert isinstance(token, str)
    
    
@pytest.mark.asyncio
async def test_create_refresh_token(mock_auth, mock_db, mock_redis):
    mock_auth.SECRET_KEY = "test_secret"
    mock_auth.ALGORITHM = "HS256"
    data = {"sub": "test@example.com"}
    expires_delta = 86400

    token = await mock_auth.create_refresh_token(data, expires_delta)

    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_decode_refresh_token(mock_auth, mock_db, mock_redis):
    mock_auth.SECRET_KEY = "test_secret"
    mock_auth.ALGORITHM = "HS256"
    data = {"sub": "test@example.com"}
    expires_delta = 86400

    refresh_token = await mock_auth.create_refresh_token(data, expires_delta)
    decoded_email = await mock_auth.decode_refresh_token(refresh_token)

    assert decoded_email == "test@example.com"

@pytest.mark.asyncio
async def test_check_role(mock_auth, mock_db, mock_redis):
    mock_user = User(id=1, email="test@example.com", role="user")

    with pytest.raises(HTTPException) as exc_info:
        await mock_auth.check_role(mock_user, "admin")
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Operation not permitted"


if __name__ == "__main__":
    pytest.main()

