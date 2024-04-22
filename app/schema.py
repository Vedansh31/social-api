from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import conint, Annotated
#A schema of the API
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# Getting a response of the user info
class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# Getting a response of post info
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True

# Getting a response with total no. of votes attached to post info
class PostVote(PostBase):
    Post: Post
    votes: int

    class Config():
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

    class Config:
        orm_mode = True
    
class Vote(BaseModel):
    post_id: int
    dir = conint(le= 1)
