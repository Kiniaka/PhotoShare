from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


# '''------------------------Images-------------------------'''


class ImageModel(BaseModel):
    """
    Image Model
    :param image_name:str: image name
    :param image_link:str: link to the image
    :param user_id: int: user id whose create the picture
    :param tags: tags 
    """
    image_name: str
    image_link: str
    user_id: int
    tags: Optional[List[int]]


class ImageUpdate(BaseModel):
    """
    Image Update Model
    :param image_name: str: image name
    :param image_link: str: link to the image
    :param tags: str: tags
    """
    image_name: Optional[str]
    image_link: Optional[str]
    tags: Optional[List[int]]


class ImageInDB(ImageModel):
    """
    Image Model in DB ?????????????????????????????????????????????????????????????????????????
    :param id: int: image id
    """
    id: int

    class Config:
        orm_mode = True


# '''------------------------Notes--------------------------'''

class NoteModel(BaseModel):
    """
    Note Model
    :param note_description:str: comment to the image
    :param image_id: int: image id
    """
    note_description: str
    image_id: int


class NoteUpdate(BaseModel):
    """
    Note Update Model
    :param updated_at: datetime: image update time and date
    """
    note_description: str
    updated_at: datetime

    class Config:
        orm_mode = True


class NoteCreate(BaseModel):
    """Schema for creating a new note."""

    note_description: str

    class Config:
        """Pydantic model configuration."""
        orm_mode = True


# '''------------------------Tags---------------------------'''


class TagModel(BaseModel):
    """
    Tag Model 
    :param tag_name: str: tag name
    :param user_id: int: user id
    """
    tag_name: str = Field(details='tags names divided by space (" ")')
    user_id: int


# '''------------------------Users--------------------------'''


class UserModel(BaseModel):
    """
    User Model
    :param username: str: user name
    :param email: user mail address
    :param password: str: user password
    """
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr
    password: str = Field(min_length=5, max_length=15)


class UserDB(UserModel):
    """
    User Model in DB 
    :param id: int: user id
    :param username: str: username
    :param email: user mail address
    :param password: str: user password
    :param avatar: str: link to user avatar
    """
    id: int
    username: str
    email: EmailStr
    password: str
    avatar: Optional[str]

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    """
    User Response Model
    :param user: body of the user from USerModel
    :param detail: str: information that the user has been created
    """
    user: UserDB
    detail: str = 'User successfully created'


# '''------------------------Tokens---------------------------'''


class TokenModel(BaseModel):
    """
    Token Model
    :param access_token: str: user access token
    :param refresh_token: str: user refresh token
    :param token_type: str: type of the token is 'bearer'
    """
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


# '''------------------------Opinion---------------------------'''


class Opinion(BaseModel):
    """
    Opinion Model
    :param vote: int : user opinion about the selected image. Accepted only numbers: 1,2,3,4,5 where 1 means the worst image and 5 means the best image.
    :param image_id: the unique image number
    """
    vote: int
    image_id: int
