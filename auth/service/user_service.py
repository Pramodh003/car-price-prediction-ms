from fastapi import HTTPException, Depends, status
from ..models import User

def user_create(user, db):
    email = db.query(User).filter(User.email == user.email).first()
    if email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This email already exist"
        )
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user