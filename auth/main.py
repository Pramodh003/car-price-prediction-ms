from .schemas import UserCreate
import uvicorn
from .models import User
from .database import Base, engine, SessionLocal,get_db
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .utils import hash, verify
from .oauth2 import create_access_token, verify_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

Base.metadata.create_all(engine)

app = FastAPI()

@app.post("/register")
async def register_user(user: UserCreate,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")
    encrypted_password = hash(user.password)
    new_user = User(email = user.email, password = encrypted_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}
    
@app.post("/login")   
async def login(user_credentials: OAuth2PasswordRequestForm =  Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
    if not verify:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
    access_token = create_access_token(data= {"user_id": user.id})
    return {"access_token": access_token, "token_type":"bearer"}


if __name__=="__main__":
     uvicorn.run("main:app", host="0.0.0.0", port=8000)