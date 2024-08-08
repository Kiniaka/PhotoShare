from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_app.src.conf.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    """
    Provides a database session to be used in a dependency injection context.

    This function is intended to be used with FastAPI's dependency injection system.
    It yields a SQLAlchemy session that is automatically closed after the request is finished.

    :yield: A SQLAlchemy database session.
    :rtype: sqlalchemy.orm.Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
