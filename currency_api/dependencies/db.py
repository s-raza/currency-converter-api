from typing import AsyncGenerator

from db.currency_db import CurrencyDB
from db.database import get_db


async def get_currency_db() -> AsyncGenerator[CurrencyDB, None]:
    db = await get_db(CurrencyDB)
    try:
        yield db
    finally:
        await db.session.close()
