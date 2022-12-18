import pytest_asyncio

from db.currency_db import CurrencyDB
from db.database import get_db
from utils import logger

tests_logger = logger.get_logger("Database")


@pytest_asyncio.fixture(scope="session")
async def db(db_engine):

    tests_logger.info("Opening DB connection and starting tests")

    currency_db = await get_db(CurrencyDB, db_engine)

    yield currency_db

    await currency_db.session.close()
    await db_engine.dispose()

    tests_logger.info("Tests completed, DB connection closed")
