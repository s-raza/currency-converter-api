import asyncio
import os

import pytest
import pytest_asyncio
from python_on_whales import docker

from db.currency_db import CurrencyDB
from db.database import create_all, get_db, get_engine
from db.models import Base
from utils import logger

tests_logger = logger.get_logger("Tests")


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="module")
async def db_engine(request):

    os.chdir(request.fspath.dirname)
    tests_logger.info("Starting MySQL container")

    docker.compose.down(volumes=True)
    docker.compose.up(detach=True)

    tests_logger.info("Container startup initiated")

    docker_config = docker.compose.config().services["test_mysqldb"]
    env = docker_config.environment
    port = docker_config.ports[0].published

    env = {k.split("_")[1].lower(): v for k, v in env.items()}
    env["port"] = port

    engine = get_engine(env)
    await create_all(engine, Base)

    yield engine

    tests_logger.info("Stopping MySQL container")
    docker.compose.down(volumes=True)

    tests_logger.info("Stopped")
    os.chdir(request.config.invocation_dir)


@pytest_asyncio.fixture(scope="module")
async def db(db_engine):

    tests_logger.info("Opening DB connection and starting tests")

    currency_db = await get_db(CurrencyDB, db_engine)

    yield currency_db

    await currency_db.session.close()
    await db_engine.dispose()

    tests_logger.info("Tests completed, DB connection closed")
