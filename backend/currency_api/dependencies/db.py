from typing import AsyncGenerator

from db.currency_db import CurrencyDB
from db.database import get_db


async def get_currency_db() -> AsyncGenerator[CurrencyDB, None]:
    """
    Get the async DB object to interact with the database using the database interface
    Class.

    This is to be used with ``fastapi.Depends()`` using dependency injection
    functionality of ``fastapi``

    :return: :obj:`AsyncGenerator` for py:obj:`db.CurrencyDB`
    """
    db = await get_db(CurrencyDB)
    try:
        yield db
    finally:
        await db.session.close()
