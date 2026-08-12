from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    is_active: bool = True

class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    is_active : bool = True
    created_at : datetime

    class Config():
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserQuestion(BaseModel):
    question: str