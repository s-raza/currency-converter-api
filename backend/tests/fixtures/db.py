import pytest_asyncio

from db.currency_db import CurrencyDB
from db.database import create_all, get_db, get_engine
from db.models import Base
from utils import logger

tests_logger = logger.get_logger("Database")


@pytest_asyncio.fixture(scope="module")
async def db(docker_env):

    engine = get_engine(docker_env)
    await create_all(engine, Base)

    tests_logger.info("Opening DB connection")
    currency_db = await get_db(CurrencyDB, engine)

    yield currency_db

    await currency_db.session.close()
    await engine.dispose()

    tests_logger.info("Test completed, DB connection closed")
