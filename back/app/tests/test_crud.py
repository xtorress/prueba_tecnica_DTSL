import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas import UserCreate
from app.crud.user import create_user, get_user_by_email
from app.models import User

@pytest.mark.asyncio
async def test_create_user(async_session: AsyncSession):
    user = UserCreate(
        username="juanito",
        email="juan@test.com",
        password="12345678"
    )
    await create_user(async_session, user)

    stmt = select(User).where(User.email == user.email)
    result = await async_session.execute(stmt)
    user_db = result.scalar_one_or_none()

    assert user_db is not None, "User not created."
    assert isinstance(user_db, User)
    assert user_db.username == user.username
    assert user_db.email == user.email
    assert user_db.hashed_password != user.password

@pytest.mark.asyncio
async def test_get_user_by_email(async_session: AsyncSession):
    user = UserCreate(
        username="juanito",
        email="juan@test.com",
        password="12345678"
    )
    new_user = await create_user(async_session, user)
    user_db = await get_user_by_email(async_session, new_user.email)

    assert user_db is not None
    assert user_db.id == 1
    assert user_db.email == "juan@test.com"