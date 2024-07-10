from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class User(BaseModel):
    id: int
    email: EmailStr
    date_created: datetime
    date_modified: datetime
    
    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]= None

