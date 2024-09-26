# Standard Library
from contextlib import asynccontextmanager
from typing import Optional

# Third Party Library
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

__all__ = (
    'create_session',
    'init_db',
    'create_engine',
)

_engine: Optional[AsyncEngine] = None
_Session: Optional[sessionmaker] = None


def create_engine(database_dsn: PostgresDsn) -> AsyncEngine:
    global _engine

    if not _engine:
        _engine = create_async_engine(
            database_dsn,
            pool_pre_ping=True
        )

    return _engine


def init_db(database_dsn: PostgresDsn):
    global _Session
    create_engine(database_dsn)

    if not _Session:
        _Session = sessionmaker(
            bind=_engine,
            expire_on_commit=False,
            class_=AsyncSession
        )


@asynccontextmanager
async def create_session(session=None, **kwargs):
    if session:
        yield session
    else:
        async with _Session(**kwargs) as session:
            yield session
