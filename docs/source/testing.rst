Testing
=======

Tests are implemented using Python's pytest module and a live MySQL server using docker.

A docker container is started upon initiating tests using pytest.

Pytest waits for the docker container to startup before connecting to it, and executing the tests using the MySQL server running inside it.

Example run:

.. code-block:: bash

    >pytest -s
    ======= test session starts =======
    platform win32 -- Python 3.9.5, pytest-7.1.2, pluggy-1.0.0
    rootdir: C:\currency-converter
    plugins: anyio-3.6.1, asyncio-0.19.0, cov-2.12.1
    asyncio: mode=strict
    collected 7 items

    tests\test_db.py 25-Jul-2022 06:49:44PM [INFO] Tests: Starting MySQL container
    26-Jul-2022 06:49:48PM [INFO] Tests: Container startup initiated
    26-Jul-2022 06:49:49PM [INFO] Engine Connection: Waiting for Database container to finish startup
    26-Jul-2022 06:49:54PM [INFO] Engine Connection: Waiting for Database container to finish startup
    26-Jul-2022 06:49:59PM [INFO] Engine Connection: Waiting for Database container to finish startup
    26-Jul-2022 06:50:04PM [INFO] Engine Connection: Waiting for Database container to finish startup
    26-Jul-2022 06:50:09PM [INFO] Engine Connection: Waiting for Database container to finish startup
    26-Jul-2022 06:50:14PM [INFO] Engine Connection: Waiting for Database container to finish startup
    26-Jul-2022 06:50:19PM [INFO] Engine Connection: Waiting for Database container to finish startup
    26-Jul-2022 06:50:26PM [INFO] Tests: Opening DB connection and starting tests
    .......26-Jul-2022 06:50:30PM [INFO] Tests: Tests completed, DB connection closed
    26-Jul-2022 06:50:30PM [INFO] Tests: Stopping MySQL container
    26-Jul-2022 06:50:34PM [INFO] Tests: Stopped


    ======= 7 passed in 14.57s =======
