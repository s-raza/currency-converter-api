import asyncio
import os

import pytest

os.environ["ENV_FILE"] = "./tests/.env"


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


pytest_plugins = ["tests.fixtures.docker", "tests.fixtures.db", "tests.fixtures.api"]
