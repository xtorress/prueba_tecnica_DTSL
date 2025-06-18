import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.models import Base
from app.core.config import settings

DATABASE_URI_TEST = settings.DATABASE_URI + "_test"

# Create a session fixture to avoid errors with the event loop.
@pytest_asyncio.fixture()
async def async_session():
    engine = create_async_engine(DATABASE_URI_TEST, echo=False)
    SessionLocalTest = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocalTest() as session:
        yield session

    await engine.dispose()



