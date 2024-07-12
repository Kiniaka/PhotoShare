from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, func, Table
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship, sessionmaker, Session
from db import Base, engine, get_db
from datetime import datetime


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
    :param role: str: user role: admin, moderator or standard user

    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True, default="test")
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    mail_confirmed = Column(Boolean, default=False)
    role = Column(String)


image_m2m_tag = Table(
    "image_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Image(Base):
    """Class which describes table in database of the Image
    :param id:int: image unique id in DB
    :param image_name: str: name of the image which is putting in DB
    :param image_link: link to the image
    :param created_at: date: the date of the image creation - format: YYYY-MM-DD HH:MM:SS where Y-means year, M - means month, D- means day H - means hour, M - means minutes and S - means secunds
    :param update_at: date: the date of the image updating - format: YYYY-MM-DD HH:MM:SS where Y-means year, M - means month, D- means day H - means hour, M - means minutes and S - means secunds
    :param user_id: int: Id number of the user who entered the image into the DB
    :param tags: tags about the image which is putting in DB. Relation 'mamy to many' - many tags to one images and one tag to many images.
    :param note: the comment about the image which is putting in DB. Relation 'many to one' - many comments to one image.  
    """
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String(50))
    image_link = Column(String(250))
    created_at = Column(DateTime)
    update_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    tags = relationship("Tag", secondary=image_m2m_tag, backref="images")
    note = relationship('Note', backref='images')


class Note(Base):
    """Class which describes table in database of the Comment
    :param id:int: note's unique id in DB
    :param note_description: str: comment of the image
    :param created_at: datetime: comment creation date
    :param updated_at: datetime: comment update date
    :param user_id: int: Id number of the user who entered the note into the DB
    :param done: information whether comment has been done or not
    :param image_id: the id number of the image to which the tag is to be assigned
    """
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    note_description = Column(String(150), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    done = Column(Boolean, default=False)
    image_id = Column(Integer, ForeignKey('images.id'))


class Tag(Base):
    """Class which describes table in database of the User
    :param id:int: tag's unique id in DB
    :param tag_name: str: tag's name
    :param user_id: int: Id number of the user who entered the tag into the DB
    """
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag_name = Column(String(25), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))


Base.metadata.create_all(bind=engine)
