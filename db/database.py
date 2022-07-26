from asyncio import current_task
from typing import Any, Dict, TypeVar

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from settings import get_conn_string
from settings import settings as cfg

from .currency_db import CurrencyDB
from .utils import wait_for_db

T = TypeVar("T")


def get_engine(conn_settings: Dict[str, Any]) -> AsyncEngine:
    """
    Get SQLAlchemy :obj:`sqlalchemy.engine.base.Engine`,
    to be provided to SQLAlchemy sessions.

    :return: :obj:`sqlalchemy.engine.base.Engine`
    """
    conn_str = get_conn_string(conn_settings)
    wait_for_db(conn_settings)
    engine = create_async_engine(conn_str, future=True, pool_recycle=3600)

    return engine


async def create_all(engine: AsyncEngine, base):  # type: ignore
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)


def get_async_session(engine: AsyncEngine) -> T:

    async_session = async_scoped_session(
        sessionmaker(engine, expire_on_commit=False, class_=AsyncSession),
        scopefunc=current_task,
    )

    return async_session


async def get_db(currency_db: CurrencyDB, engine: AsyncEngine = None) -> CurrencyDB:

    if engine is None:
        engine = get_engine(cfg.db_conn_settings)

    async_session = get_async_session(engine)  # type: ignore

    async with async_session() as session:
        async with session.begin():
            return currency_db(session)  # type: ignore
