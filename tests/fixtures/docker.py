import os
import time

import pytest_asyncio
from python_on_whales import docker

from db.database import create_all, get_engine
from db.models import Base
from utils import logger

tests_logger = logger.get_logger("Docker")


@pytest_asyncio.fixture(scope="module")
async def db_engine(request):

    os.chdir(request.fspath.dirname)
    tests_logger.info("Starting Docker Containers")

    docker.compose.down(volumes=True)
    docker.compose.up(detach=True)

    tests_logger.info("Startup initiated in detached mode")

    docker_config = docker.compose.config().services["test_mysqldb"]
    env = docker_config.environment
    port = docker_config.ports[0].published

    env = {k.split("__")[1].lower(): v for k, v in env.items() if "MYSQL__" in k}
    env["port"] = port

    engine = get_engine(env)

    await create_all(engine, Base)
    time.sleep(5)

    yield engine

    tests_logger.info("Removing Containers")
    docker.compose.down(volumes=True)

    tests_logger.info("Removed")
    os.chdir(request.config.invocation_dir)
