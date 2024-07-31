from .schemas import UserCreate
import uvicorn
from auth.models import User
from auth.database import Base, engine, SessionLocal,get_db
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.utils import hash, verify
from auth.oauth2 import create_access_token, verify_access_token, get_current_user,oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from redis import red
Base.metadata.create_all(engine)
from auth.redis import redis_client

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
    redis_client.set(access_token,user.id)
    return {"access_token": access_token, "token_type":"bearer"}

@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    print(token)
    redis_client.delete(token[0])
    return {"msg": "Logout successful"}

if __name__=="__main__":
     uvicorn.run("main:app", host="0.0.0.0", port=8000)