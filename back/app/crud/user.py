from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.schemas import UserCreate, UserBase
from app.core.security import get_password_hash, check_password

async def get_user_by_email(session: AsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, user: UserCreate) -> UserCreate:
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

async def authenticate(session: AsyncSession, email: str, password: str):
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not check_password(password, user.hashed_password):
        return None
    return user