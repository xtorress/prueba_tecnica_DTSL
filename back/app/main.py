from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.db import init_db
from app.api import items, users, login

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.include_router(items.router)
app.include_router(users.router)
app.include_router(login.router)

@app.get("/")
async def root():
    return {"message": "APIs Prueba Tecnica DIVAIN."}