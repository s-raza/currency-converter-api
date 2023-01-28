Testing
=======

Tests are implemented using Python's `pytest` and a live MySQL server using docker.

Docker containers are started upon initiating tests using pytest.

Pytest waits for the docker containers to startup before connecting to them, and
executing the tests using the MySQL and FastAPI servers running inside them.

Before running tests copy the `tests/.env-template` file to `tests/.env`, all
the settings in it can be left as they are for local testing purposes.

Example Test Run
----------------

.. code-block:: text

    currency-converter-api> cd backend
    currency-converter-api\backend> pytest
    =========================== test session starts ===========================
    platform win32 -- Python 3.9.0, pytest-7.1.2, pluggy-1.0.0
    rootdir: D:\Development\currency-converter-api
    plugins: anyio-3.6.1, asyncio-0.19.0, cov-2.12.1, typeguard-2.13.3
    asyncio: mode=strict
    collected 13 items

    tests\test_api.py ....                                                                                                        [ 30%]
    tests\test_db.py .........                                                                                                    [100%]

    =========================== 13 passed in 76.00s (0:01:16) ===========================
