from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.schemas import UserCreate, UserBase
from app.utils import get_password_hashed

async def get_user_by_email(session: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, user: UserCreate) -> UserCreate:
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hashed(user.password)
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

async def authenticate(session: AsyncSession, emait: str, pasw: str):
    pass