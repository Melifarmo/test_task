from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.sqlalchemy import db_session_factory


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_session_factory() as session:
        try:
            yield session
        except Exception as exc:
            await session.rollback()
            raise exc
        else:
            await session.commit()
