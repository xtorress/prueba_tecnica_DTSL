from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item, StockHistory
from app.schemas import ItemSchema, ItemBase

class DuplicateItemError(Exception):
    def __init__(self, value: str):
        self.value = value

async def get_items(session: AsyncSession):
    stmt = select(Item)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_item_by_id(session: AsyncSession, id: int):
    stmt = select(Item).where(Item.id == id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_item_by_sku_or_ean13(session: AsyncSession, ean13: str, sku: str):
    stmt = select(Item).where((Item.ean13 == ean13 ) | (Item.sku == sku))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

# async def get_item_by_ean13(session: AsyncSession, ean13: int):
#     pass

async def create_item(session, item: ItemBase):
    exist = await get_item_by_sku_or_ean13(session, item.ean13, item.sku)
    if exist:
        if exist.ean13 == item.ean13:
            raise DuplicateItemError("ean13")
        elif exist.sku == item.sku:
            raise DuplicateItemError("sku")
    
    new_item = Item(**item.model_dump())
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item

async def update_item_stock(session: AsyncSession, item:ItemSchema, new_stock):
    """Update item stock and create a StockHistory."""
    quantity_change = new_stock - item.stock

    if quantity_change > 0:
        move = "entrada"
    elif quantity_change < 0:
        move = "salida"
    else:
        move = "igual"
    
    history = StockHistory(
        item_id = item.id,
        prev_stock = item.stock,
        actual_stock = new_stock,
        quantity_change = quantity_change,
        move = move
    )

    item.stock = new_stock
    session.add(history)
    await session.commit()
    await session.refresh(history)
    return history

async def get_histories_stock(session: AsyncSession):
    # Use selectinload because relationships in SQLAlchemy are a lazy-loaded by default.
    stmt = select(StockHistory).options(selectinload(StockHistory.item))
    result = await session.execute(stmt)
    return result.scalars().all()