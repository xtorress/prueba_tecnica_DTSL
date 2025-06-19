from typing import List
from fastapi import APIRouter,  HTTPException

from app.core.db import SessionDep
from app.schemas import ItemBase, StockHistoryBase, \
                        StockUpdateRequest
from app.crud.item import get_items, get_histories_stock, get_item_by_id, update_item_stock

router = APIRouter(prefix="/items", tags=['items'])

@router.get("/", response_model=List[ItemBase])
async def list_items(session: SessionDep):
    items = await get_items(session)
    return items

@router.get("/history", response_model=List[StockHistoryBase])
async def list_histories(session: SessionDep):
    histories = await get_histories_stock(session)
    return histories

@router.patch("/{item_id}/stock")
async def update_stock(session: SessionDep, item_id: int, data:StockUpdateRequest):
    try:
        item = await get_item_by_id(session, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item no encontrado.")
        if data.new_stock < 0:
            raise HTTPException(status_code=404, detail="El stock no puede ser negativo.")
        movement = await update_item_stock(session, item, data.new_stock)
        # await session.refresh()
        return {
            "status": 200,
            "msg":"Stock actualizado correctamente.",
            "data":movement
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=505,
            detail=f"Error al actualizar stock: {str(e)}"
        )

