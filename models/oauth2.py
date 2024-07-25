from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,status, Depends
import os 
from dotenv import load_dotenv
load_dotenv()
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError , jwt
from . import schemas
from sqlalchemy.orm import Session
from . import database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credential_exception
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user