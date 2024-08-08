from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    """
    User Model

    :param username: user name
    :type username: str
    :param email: user mail address
    :type email: EmailStr
    :param password: user password
    :type password: str
    """
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    User Model in DB

    :param id: user id
    :type id: int
    :param username: username
    :type username: str
    :param email: user mail address
    :TYPE email: EmailStr
    :param role: user role : 'admin', 'standard user' or 'modelator'
    :type role: str
    :param created_at: date of user creation
    :type created_at: datetime
    :param avatar: link to user avatar
    :type avatar: str
    """
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    """
    User Response Model

    :param user: user data
    :type user: UserDB
    :param detail: information that the user has been created
    :type detail: str
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Token Model

    :param access_token: user access token
    :type access_token: str
    :param refresh_token: user refresh token
    :type refresh_token: str
    :param token_type: type of the token is 'bearer'
    :type token_type: str
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
    Request Email Model

    :param email: email adress
    :type email: EmailStr
    """
    email: EmailStr
      
class CommentBase(BaseModel):
    """
    Commend Base Model

    :param content: comment to the photo
    :type content: str
    """
    content: str


class CommentCreate(CommentBase):
    """
    Comment Create Model
    """
    pass


class CommentUpdate(CommentBase):
    """
    Comment Update Model
    """
    pass


class Comment(CommentBase):
    """
    Comment Model

    :param id: comment id number
    :type id: int
    :param created_at: date and time of comment creation
    :type created_at: datetime
    :para updated_at: date and time the comment was updated
    :type updated_at: datetime
    :param user_id: user id
    :type user_id: int
    :param photo_id: photo id
    :type photo_id: int
    """
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    photo_id: int

    class Config:
        orm_mode = True


class PhotoBase(BaseModel):
    """
    Photo Base Model

    :param url: ulr adress to the photo
    :type url: str
    :param description: description of the selected photo
    :type description: str, optional
    :param tags: tags associated with the selected image
    :type tags: str, optional
    """
    url: str
    description: Optional[str] = None
    tags: Optional[str] 


class PhotoCreate(PhotoBase):
    """
    Photo Create Model
    """
    pass


class Photo(PhotoBase):
    """
    Photo Model

    :param id: photo's id numeber
    :type id: int
    :param user_id: user id number
    :type user_id: int
    :param created_at: date and time of photo's creation 
    :type created_at: datetime
    """
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class DescriptionSearch(BaseModel):
    """
    DescriptionSearch Model: 
    
    :param id: photo's id number
    :type id: int
    :param user_id: user's id numeber
    :type id: int
    :param url: url adress of the photo
    :type url: str
    :param description: description of the photo
    :type description: str
    :param tags: list of tags connected with the photo
    :type tags: list
    :param tags: list of tags connected with the photo
    :param created_at: the date and time of the photo's creation 
    :type: datetime
    :param updated_at: the date and time of the photo's updating 
    :type: datetime
    :param rating: rating of the photo - if the user like this photo or not.Use digits :max is 6  and min is 1.
    :type rating: int 
    """
    id: int
    user_id: int
    url: str
    description: str
    tags: list
    created_at: datetime | None
    updated_at: datetime | None
    rating: int | None
    class Config:
        orm_mode = True
 
class TagSearch(BaseModel):
    """
    TagSearch Model: 
    
    DescriptionSearch Model: 
    :param id: photo's id number
    :type id: int
    :param user_id: user's id numeber
    :type id: int
    :param url: url adress of the photo
    :type url: str
    :param description: description of the photo
    :type description: str
    :param tags: list of tags connected with the photo
    :type tags: list
    :param tags: list of tags connected with the photo
    :param created_at: the date and time of the photo's creation 
    :type: datetime
    :param updated_at: the date and time of the photo's updating 
    :type: datetime
    :param rating: rating of the photo - if the user like this photo or not.Use digits :max is 6  and min is 1.
    :type rating: int 
    """
    id: int
    user_id: int
    url: str | None
    description: str | None
    tags: list | None
    created_at: datetime | None
    updated_at: datetime | None
    rating: int | None
    class Config:
        orm_mode = True



class UserSearch(BaseModel):
    """
    User Search Model
    
    :param user_id: user's id
    :type user_id: int
    """
    user_id: int


class ProfileResponse(BaseModel):
    """
    Profile Response Model

    :param username: username
    :type username: str
    :para email: user's email addres
    :type email: EmailStr
    :param role: the role of the user: administrator, standard user or modelator
    :type role: str
    :param created_at: date and time of update
    :type created_at: datetime
    :param avatar: link to the user's avatar 
    :type avatar: str
    :param photo_amount: number of images for a selected user
    :type photo_amount: int
    """
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    avatar: str
    photo_amount: int

    class Config:
        orm_mode = True

class ProfileStatusUpdate(BaseModel):
    """
    Profile Status Update Model

    :param username: username
    :type username: str
    :param password: password of the user
    :type password: str
    :param avatar: link to the user's avatar 
    :type avater: str
     """
    username: str
    password: str
    avatar: str

