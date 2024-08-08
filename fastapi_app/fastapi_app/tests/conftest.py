import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_app.main import app
from fastapi_app.src.database.models import Base
from fastapi_app.src.database.db import get_db
from fastapi_app.src.conf.config import settings
from fastapi_app.src.database.models import User, Photo

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    

@pytest.fixture(scope="module")
def user():
    return {"username": "testuser1", "email": "testuser1@example.com", "password": "Testuser!2"}


@pytest.fixture(scope="module")
def create_test_user(session, user):
    db_user = User(
        username=user['username'],
        email=user['email'],
        hashed_password=user['password']
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# @pytest.fixture(scope="module")
# def photo():
#     return {"id":1, "url": "uploads/f5922740-e714-4983-b190-f23511e2fbe8.jpeg","user_id": 1,"description":"water","created_at":"2024-07-29T09:14:47.702008","updated_at":"2024-07-29T09:14:58.702008","rating":0}


# @pytest.fixture(scope="module")
# def create_test_photo(session, photo):
#     db_photo = Photo(
#         id=photo['id'],
#         url=photo['url'],
#         user_id=photo['user_id'],
#         description =photo['description'],
#         created_at =photo['created_at'],
#         updated_at =photo['updated_at'],
#         rating =photo['rating']
#     )
#     session.add(db_photo)
#     session.commit()
#     session.refresh(db_photo)
#     return db_photo