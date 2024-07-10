from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from ..config.database import get_db
from .. import schemas, models, utils
from ..service.user_service import user_create
from ..service.redis_service import write_to_redis 

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = user_create(user, db)
    # data = {
    #     "hashed_password": new_user.password,
    #     "id": new_user.id
    # }
    # write_to_redis(new_user.email, data)
    return new_user