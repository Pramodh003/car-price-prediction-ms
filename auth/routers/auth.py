from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models , utils, oauth2
from config import database
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=["Authentication"])

