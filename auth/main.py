from fastapi import FastAPI
from .config.database import engine
from .routers import user, auth
from . import models
from .config.config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
