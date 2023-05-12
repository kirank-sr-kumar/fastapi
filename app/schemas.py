from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class User(BaseModel):
    email: EmailStr
    id: int
    class Config():
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

    class Config():
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    vote: int
    class Config():
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password:str
    



class UserLogin(BaseModel):
    email:EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type: str

    class Config():
        orm_mode = True

class TokenData(BaseModel):
    id: Optional[str]= None

class Vote(BaseModel):
    post_id: int
    direc:int