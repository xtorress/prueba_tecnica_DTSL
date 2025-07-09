from datetime import timedelta
from typing import Annotated

from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.db import SessionDep
from app.core.config import settings
from app.core.security import create_access_token
from app.schemas import Token
from app.crud import user as crud

router = APIRouter(tags=["login"])

@router.post("/login/access-token")
async def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> Token:
    user = await crud.authenticate(
        session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    expire_time = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(user.id, expire_delta=expire_time)
    )