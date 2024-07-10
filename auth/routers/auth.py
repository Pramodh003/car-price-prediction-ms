from fastapi import Depends, APIRouter, status, HTTPException, Request
from sqlalchemy.orm import Session
from .. import schemas, models , utils, oauth2
from ..config.database import get_db
from ..config.redis_db import redis_client
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..utils import verify
from ..service.redis_service import write_to_redis
from ..oauth2 import oauth2_scheme
router = APIRouter(tags=["Authentication"])

@router.get("/")
def create_end():
    return {"msg": "Server is Up"}

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    id = utils.verify(user_credentials.username, user_credentials.password, db)
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User could not found"
        )
    if not id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    access_token = oauth2.create_access_token(data={"user_id": id})
    write_to_redis(access_token,id)
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    redis_client.delete(token)
    return {"message": "Successfully logged out"}
