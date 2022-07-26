import time
from asyncio import current_task
from typing import Any, Dict, List, TypeVar

import pymysql  # type: ignore
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from db.currency_db import CurrencyDB
from settings import get_conn_string
from utils import logger

engine_logger = logger.get_logger("Engine Connection")

T = TypeVar("T")


def wait_for_db(
    conn_settings: Dict[str, Any], sleep: int = 5, extra_sleep: int = 0
) -> bool:
    """
    Attempts to connect to the database indefinitely,
    in case the database is not yet up.

    While attempting to connect, displays reason for delay in  connecting.

    :param conn_settings: Dictionary containing the setting:value pairs
    :type conn_settings: required

    :param sleep: Number of seconds between reconnection attempts.
    :type sleep: optional, default=5

    :param extra_sleep: Extra seconds to sleep after a successful connection.
    :type extra_sleep: optional

    """

    settings: List[Any] = ["user", "password", "database", "host", "port"]

    conn_settings = {k: conn_settings[k] for k in settings}
    conn_settings["port"] = int(conn_settings["port"])

    connected = False
    while not connected:
        try:
            connection = pymysql.connect(**conn_settings)
            if connection.open:
                connected = True
        except Exception as e:
            if e.args[0] in [2003, 2013]:
                engine_logger.info("Waiting for Database container to finish startup")
            else:
                engine_logger.info(f"Exception: {e.args}")
            time.sleep(sleep)
            continue

    if extra_sleep != 0:
        time.sleep(extra_sleep)

    return True


async def get_engine(conn_settings: Dict[str, Any], base: Any) -> AsyncEngine:
    """
    Get SQLAlchemy :obj:`sqlalchemy.engine.base.Engine`,
    to be provided to SQLAlchemy sessions.

    :return: :obj:`sqlalchemy.engine.base.Engine`
    """
    conn_str = get_conn_string(conn_settings)

    wait_for_db(conn_settings)

    engine = create_async_engine(conn_str, future=True, pool_recycle=3600)

    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

    return engine


async def get_async_db(engine: AsyncEngine, currency_db: CurrencyDB) -> T:

    async_session = async_scoped_session(
        sessionmaker(engine, expire_on_commit=False, class_=AsyncSession),
        scopefunc=current_task,
    )

    async with async_session() as session:
        async with session.begin():
            return currency_db(session, engine)  # type: ignore
