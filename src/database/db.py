from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path


path = '.env'

load_dotenv(path)
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{os.getenv("POSTGRES_USERNAME")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("HOST")}:{os.getenv("PORT_NR")}/{os.getenv("DATABASE_NAME")}'
# fake data for sphinx to avoid None data during doc generation
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """funtion connects to database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
