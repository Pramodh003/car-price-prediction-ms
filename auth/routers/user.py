from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from config.database import get_db
from .. import schemas, database, models, utils
from service.user_service import user_create

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = u