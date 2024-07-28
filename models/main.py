from fastapi import Depends , Response, APIRouter , HTTPException, status,FastAPI
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . import models
from .database import get_db
from . import models,schemas, oauth2
from typing import List, Optional
import pika
import os
from dotenv import load_dotenv
import requests
import uvicorn
from models.rpc import get_rabbitmq_connection

app = FastAPI()
load_dotenv(".env")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
AUTH_BASE_URL = os.getenv("AUTH_BASE_URL")


@app.post("/login", tags=['Authentication Service'])
async def login(user_data: schemas.User):
    try:
        response = requests.post(f"{AUTH_BASE_URL}/login", json={"username": user_data.username, "password": user_data.password})
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")

@app.post("/register", tags=['Authentication Service'])
async def registeration(user_data: schemas.UserCreate):
    try:
        response = requests.post(f"{AUTH_BASE_URL}/api/users", json={"email": user_data.email, "password": user_data.password})
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")
    

@app.get("/vehicle")
def vehicle():
    return {"message":"Gateway app is live"}

@app.post("/vehicle",status_code=status.HTTP_201_CREATED,response_model=schemas.Item)
def add_vehicle(vehicle: schemas.ItemCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    vehicle_add = models.Vehicle(owner_id=current_user.id,**vehicle.dict())
    db.add(vehicle_add)
    db.commit()
    db.refresh(vehicle_add)
    id = vehicle_add.id
    connection, channel = get_rabbitmq_connection()
    channel.basic_publish(
        exchange='',
        routing_key='vehicle_queue',
        body=str(id)
    )
    print("Message sent successfully")
    connection.close()
    
    return vehicle_add

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

