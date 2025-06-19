from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item, StockHistory
from app.schemas import StockHistoryBase, ItemSchema

async def list_items(session: AsyncSession):
    stmt = select(Item)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_item_by_id(session: AsyncSession, id: int):
    stmt = select(Item).where(Item.id == id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def update_item_stock(session: AsyncSession, item:ItemSchema, new_stock):
    quantity_change = item.stock - new_stock

    if quantity_change > 0:
        move = "entrada"
    elif quantity_change < 0:
        move = "salida"
    
    history = StockHistoryBase(
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

async def list_history_stock(session: AsyncSession):
    stmt = select(StockHistory)
    result = await session.execute(stmt)
    return result.scalars().all()