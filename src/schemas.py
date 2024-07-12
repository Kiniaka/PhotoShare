from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

'''------------------------Images-------------------------'''

class ImageModel(BaseModel):
    image_name: str
    image_link: str
    user_id: int
    tags: Optional[List[int]]

class ImageUpdate(BaseModel):
    image_name: Optional[str]
    image_link: Optional[str]
    tags: Optional[List[int]]

class ImageInDB(ImageModel):
    id: int

    class Config:
        orm_mode = True

'''------------------------Notes--------------------------'''

class NoteModel(BaseModel):
    description: str
    image_id: int

class NoteUpdate(NoteModel):
    updated_at: datetime

'''------------------------Tags---------------------------'''

class TagModel(BaseModel):
    tag_name: str
    user_id: int

'''------------------------Users--------------------------'''

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=20)
    email: EmailStr
    password: str = Field(min_length=5, max_length=15)

class UserDB(UserModel):
    id: int
    username: str
    email: EmailStr
    password: str
    avatar: Optional[str]

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    user: UserDB
    detail: str = 'User succesfully created'

'''------------------------Tags---------------------------'''

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
