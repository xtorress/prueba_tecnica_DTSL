from fastapi import APIRouter,  HTTPException

from app.core.db import SessionDep
from app.schemas import UserCreate
from app.crud import user as crud

router = APIRouter(prefix="/users", tags=['users'])

@router.post("/")
async def create_user(session: SessionDep, user_in: UserCreate):
    try:
        user = await crud.get_user_by_email(session, user_in.email)
        if user:
            raise HTTPException(status_code=400, detail="Email ya existe.")
        user = await crud.create_user(session, user_in)
        return {
            "msg": "Usuario creado correctamente.",
            "data": user
        }
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear usuario: {str(e)}"
        )
