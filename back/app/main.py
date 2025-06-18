from fastapi import FastAPI
from contextlib import asynccontextmanager

import app.models
from app.core.config import settings
from app.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
# @app.on_event("startup")
# def on_startup():
#     init_db()
