from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    
    
class ItemBase(BaseModel):
    symboling: int
    CarName: str
    fueltype: str
    aspiration: str
    doornumber: int
    carbody: str
    drivewheel: str
    enginelocation: str
    wheelbase: float
    carlength: float
    carwidth: float
    carheight: float
    curbweight: float
    enginetype: str
    cylindernumber: int
    enginesize: int
    fuelsystem: str
    boreratio: float
    stroke: float
    compressionratio: float
    horsepower: int
    peakrpm: int
    citympg: int
    highwaympg: int
    price: Optional[float] = None


class ItemCreate(ItemBase):
    pass

class PredictBase(BaseModel):
    price: float
    class Config:
        orm_mode = True
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        orm_mode = True    
    
class Item(ItemBase):
    id: str
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True


    
class UserCreate(User):
    pass
    class Config:
        orm_mode=True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None