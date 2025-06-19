import pytest
from sqlalchemy import text
from app.core.db import engine, init_db

@pytest.mark.asyncio
async def test_database_connection():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1
    except Exception as e:
        pytest.fail(f"Fallo la conexión a la base de datos: {e}")

# @pytest.mark.asyncio
# async def test_init_db():
#     try:
#         await init_db()
#     except Exception as e:
#         pytest.fail(f"init_db falló: {e}")