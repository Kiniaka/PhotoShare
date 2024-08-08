from sqlalchemy import Column, Integer, String, Boolean, func, Table, UniqueConstraint, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

photo_tag_table = Table(
    'photo_tag', Base.metadata,
    Column('photo_id', Integer, ForeignKey('photos.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    """Class which describes table in database of the User

    :param id: User unique id in DB
    :type id: int
    :param username: Username
    :type username: str:
    :param email: mail address of the user
    :type email: str:
    :param password: user password
    :type password: str:
    :param role: user role: admin, moderator or standard user
    :type role: str:
    :param created_at: the date of user creation
    :type created_at: datetime:
    :param avatar: link to the image of avatar in Cloudinary
    :type avatar: str:
    :param refresh_token: refresh_token of the user
    :type refresh_token: str: 
    :param confirmed: information if the user is confirmed by mail
    :type confirmed: boolean:
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String, default="user")
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    comments = relationship("Comment", back_populates="user")
    photos = relationship("Photo", back_populates="user")

class Photo(Base):
    """Class which describes table in database of the Photo

    :param id: photo unique id in DB
    :type id: int
    :param user_id: id number of the user who entered the image into the DB
    :type user_id: int
    :param url: url adress to the photo
    :type url: str
    :param description: description of the photo
    :type description: str
    :param tags: tags about the photo which is putting in DB. Relation 'many to many' - many tags to one photo and one tag to many photos.
    :type tags: relations
    :param created_at: the date and time of the photo creation - format: YYYY-MM-DD HH:MM:SS where Y-means year, M - means month, D- means day H - means hour, M - means minutes and S - means seconds
    :type created_at: datetime
    :param updated_at: the date and time of the photo updating - format: YYYY-MM-DD HH:MM:SS where Y-means year, M - means month, D- means day H - means hour, M - means minutes and S - means seconds
    :type updated_at: datetime
    :param rating: rating
    :type rating: float
    """
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String)
    description = Column(String)
    tags = relationship("Tag", secondary=photo_tag_table)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=None, onupdate=func.now())
    rating = Column(Float, default=0.0)
    user = relationship("User", back_populates="photos")
    comments = relationship("Comment", back_populates="photo", cascade="all, delete")

class Tag(Base):
    """
    Class which describes table in database of the Tag

    :param id: tag's unique id in DB
    :type id: int
    :param name: tag's name
    :type name: str
    :param user_id: id number of the user who entered the tag into the DB
    :type user_id: int
    """
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

class Comment(Base):
    """Class which describes table in database of the Comment

    :param id: comment's unique id in DB
    :type id: int
    :param photo_id: the id number of the photo to which the tag is to be assigned
    :type photo_id: int
    :param user_id: Id number of the user who entered the note into the DB
    :type user_id: int
    :param content: comment of the photo
    :type content: str
    :param created_at: comment creation date
    :type created_at: datetime
    :param updated_at: datetime: comment update date
    :type updated_at: datetime
    """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey('photos.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="comments")
    photo = relationship("Photo", back_populates="comments")


class Opinion(Base):
    """
    Class which archives all opinion about photos
    
    :param id: opinion's unique id in DB
    :type id: int
    :param vote: number of stars which show how the photo user loved
    :type vote: int
    :param user_id: id number of the user who voted
    :type user_id: int
    :param photo_id: photo unique id in DB
    :type photo_id: int
    """
    __tablename__ = "opinions"
    id = Column(Integer, primary_key=True, index=True)
    vote = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    photo_id = Column(Integer, ForeignKey("photos.id", ondelete="CASCADE"))