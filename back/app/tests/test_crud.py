import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas import UserCreate
from app.crud.user import create_user, get_user_by_email, authenticate
from app.crud.item import get_items, get_item_by_id, update_item_stock, get_histories_stock
from app.models import User, Item

@pytest.fixture
def user():
    return UserCreate(
        username="juanito",
        email="juan@test.com",
        password="12345678"
    )

@pytest.fixture
def item():
    return {
        "name": "camisa azul",
        "sku": "camisa-azul-m",
        "ean13": "1234567891234",
        "stock": 13
    }

# User tests.

@pytest.mark.asyncio
async def test_create_user(async_session: AsyncSession, user):
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
async def test_get_user_by_email(async_session: AsyncSession, user):
    new_user = await create_user(async_session, user)
    user_db = await get_user_by_email(async_session, new_user.email)

    assert user_db is not None
    assert user_db.id == 1
    assert user_db.email == "juan@test.com"

@pytest.mark.asyncio
async def test_authenticate(async_session: AsyncSession, user):
    await create_user(async_session, user)

    user_db = await authenticate(async_session, "juan@test.com", "12345678")
    
    assert user_db is not None
    assert user_db.email == "juan@test.com"

@pytest.mark.asyncio
async def test_authtenticate_fail_email(async_session: AsyncSession):
    user_db = await authenticate(async_session, "j@test.com", "12345678")
    assert user_db is None

@pytest.mark.asyncio
async def test_authenticate_invalid_password(async_session, user):
    await create_user(async_session, user)
    user_db = await authenticate(async_session, "juan@test.com", "error12345")
    assert user_db is None


## Item tests.

@pytest.mark.asyncio
async def test_get_items_empty(async_session: AsyncSession):
    items = await get_items(async_session)
    assert items == []


@pytest.mark.asyncio
async def test_get_item_by_id(async_session: AsyncSession, item):
    new_item = Item(**item)
    async_session.add(new_item)
    await async_session.commit()
    await async_session.refresh(new_item)

    item_db = await get_item_by_id(async_session, 1)
    assert item_db is not None
    assert item_db.id == 1
    assert item_db.name == "camisa azul"


@pytest.mark.asyncio
async def test_update_item_stock(async_session: AsyncSession, item):
    new_item = Item(**item)
    async_session.add(new_item)
    await async_session.commit()
    await async_session.refresh(new_item)

    history = await update_item_stock(async_session, new_item, new_stock=20)

    assert history is not None
    assert history.item_id == 1
    assert history.prev_stock == 13
    assert history.actual_stock == 20
    assert history.quantity_change == 7
    assert history.move == "entrada"

    # Verify that the item's stock is also being updated.
    updated_item = await get_item_by_id(async_session, 1)
    assert updated_item.stock == 20


@pytest.mark.asyncio
async def test_get_histories_stock(async_session: AsyncSession, item):
    new_item = Item(**item)
    async_session.add(new_item)
    await async_session.commit()
    await async_session.refresh(new_item)

    await update_item_stock(async_session, new_item, new_stock=25)

    history_list = await get_histories_stock(async_session)
    assert len(history_list) == 1
    assert history_list[0].item_id == 1
    assert history_list[0].quantity_change == 12