import time
from typing import Any, Dict, List, TypeVar

import pymysql  # type: ignore

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
                engine_logger.info(f"Waiting for Database: {e.args}")
            else:
                engine_logger.info(f"Exception: {e.args}")
            time.sleep(sleep)
            continue

    if extra_sleep != 0:
        time.sleep(extra_sleep)

    return True
