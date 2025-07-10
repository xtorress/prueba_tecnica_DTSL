from typing import Annotated
import jwt
from jwt import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.db import SessionDep
from app.core.config import settings
from app.schemas import TokenData, UserBase
from app.crud import user as crud

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login/access-token")

async def get_current_user(
        session: SessionDep, token: Annotated[str, Depends(oauth2_schema)]
    ) -> UserBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid Token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, security.ALGORITHM)
        token_data = TokenData(**decoded)
        print(decoded)
        if token_data.sub is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await crud.get_user_by_email(session, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

current_user = Annotated[UserBase, Depends(get_current_user)]