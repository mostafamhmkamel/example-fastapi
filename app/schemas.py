from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

# the purpose of the code below is to define how we want users to enter and receive data


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    class Config():
        from_attributes = True

#the below makes sure that the post is in the correct data type
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase): #by default, since we have PostBase inside, it will inherit the above fields
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config():
        from_attributes = True
    
class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config():
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id : int
    dir: int #conint(le=1)
