from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.sql.schema import ForeignKey
import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy.sql.sqltypes import DateTime
from datetime import datetime

path = '.env'

load_dotenv(path)
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{os.getenv("POSTGRES_USERNAME")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("HOST")}:{os.getenv("PORT_NR")}/{os.getenv("DATABASE_NAME")}'
# fake data for sphinx to avoid None data during doc generation
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """Class which describes table in database of the User
    :param id:int: User unique id in DB
    :param username: str: Username
    :param email: str: mail adress of the user
    :param created_at: datetime: the date of user creation
    :param avatar: str: link to the image of awatar in clouddinary
    :param password: str: user password
    :param refresh_token: str: refresh_token
    :param mail_confirmed: boolean: information if the mail of the user is confirmed by mail

    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    created_at = Column('crated_at', DateTime, default=datetime.now())
    avatar = Column(String(255), nullable=True, default="test")
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    mail_confirmed = Column(Boolean, default=False)


class Image(Base):
    """Class which describes table in database of the Image
    :param id:int: Image unique id in DB
    :param picture_name: str: name of the picture which is putting in DB
    :param created_at: date: the date of the picture creation date- format: YYYY-MM-DD where Y-means year, M - means month and D- means day
    :param updated_at: date: the date of the picture updating date- format: YYYY-MM-DD where Y-means year, M - means month and D- means day
    :param tag: str: tag
    :param comment: str: short comment about the image which is putting in DB
    :param user_id: int: Id number of the user who entered the given person into the DB
    """
    __tablename__ = "images"
    # id = Column(Integer, primary_key=True, index=True)
    # picture_name = Column(String(50))
    # created_at = Column(Date)
    # update_at = Column(Date)
    # tag = Column(String(50))
    # comment = Column(String, default=None)
    # user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))


Base.metadata.create_all(bind=engine)


def get_db():
    """funtion connects to database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
