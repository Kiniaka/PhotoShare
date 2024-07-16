from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = (
    f'postgresql+psycopg2://{os.getenv("POSTGRES_USERNAME")}:'
    f'{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("HOST")}:'
    f'{os.getenv("PORT_NR")}/{os.getenv("DATABASE_NAME")}'
)

# fake data for sphinx to avoid None data during doc generation
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Function that connects to the database and returns a session.
    Use this function as a context manager to manage the session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
