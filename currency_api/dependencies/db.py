from db.currency_db import CurrencyDB
from db.models import Base
from db.utils import get_async_db, get_engine
from settings import settings as cfg


async def get_currency_db() -> CurrencyDB:

    engine = await get_engine(cfg.db_conn_settings, Base)
    return await get_async_db(engine, CurrencyDB)  # type: ignore
