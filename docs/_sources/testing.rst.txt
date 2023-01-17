Testing
=======

Tests are implemented using Python's pytest module and a live MySQL server using docker.

A docker container is started upon initiating tests using pytest.

Pytest waits for the docker container to startup before connecting to it, and executing the tests using the MySQL server running inside it.

Example run:

.. code-block:: bash

    > pytest -s -v
    ======================================================= test session starts ========================================================
    platform win32 -- Python 3.9.0, pytest-7.1.2, pluggy-1.0.0 -- C:\.python_venvs\poetry\cache\virtualenvs\currency-converter-api-CRVacMOl-py3.9\Scripts\python.exe
    cachedir: .pytest_cache
    rootdir: D:\Development\currency-converter-api
    plugins: anyio-3.6.1, asyncio-0.19.0, cov-2.12.1, typeguard-2.13.3
    asyncio: mode=strict
    collected 13 items

    tests/test_api.py::test_api_currencies_list 02-Jan-2023 04:37:14PM [INFO] Docker: Starting Docker Containers
    failed to get console mode for stderr: The handle is invalid.
    [+] Building 4.1s (22/22) FINISHED
    => [internal] load build definition from Dockerfile.api                                                                        0.0s
    => => transferring dockerfile: 1.26kB                                                                                          0.0s
    => [internal] load .dockerignore                                                                                               0.0s
    => => transferring context: 34B                                                                                                0.0s
    => [internal] load metadata for docker.io/library/python:3.9.16-slim                                                           2.9s
    => [ 1/17] FROM docker.io/library/python:3.9.16-slim@sha256:9e0b4391fc41bc35c16caef4740736b6b349f6626fd14eba32793ae3c7b01908   0.0s
    => => resolve docker.io/library/python:3.9.16-slim@sha256:9e0b4391fc41bc35c16caef4740736b6b349f6626fd14eba32793ae3c7b01908     0.0s
    => [internal] load build context                                                                                               0.1s
    => => transferring context: 210.40kB                                                                                           0.1s
    => CACHED [ 2/17] RUN apt-get update; apt-get install curl -y                                                                  0.0s
    => CACHED [ 3/17] RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry POETRY_VERSION=1.2.0 python &&     0.0s
    => CACHED [ 4/17] RUN groupadd -r appgrp                                                                                       0.0s
    => CACHED [ 5/17] RUN useradd -r -m appusr                                                                                     0.0s
    => CACHED [ 6/17] RUN usermod -a -G appgrp appusr                                                                              0.0s
    => CACHED [ 7/17] WORKDIR /app                                                                                                 0.0s
    => CACHED [ 8/17] RUN chown appusr:appgrp /app                                                                                 0.0s
    => CACHED [ 9/17] COPY --chown=appusr:appgrp ./pyproject.toml ./poetry.lock* ./                                                0.0s
    => CACHED [10/17] RUN poetry install --no-root --no-dev                                                                        0.0s
    => [11/17] COPY --chown=appusr:appgrp ./currency_api ./currency_api                                                            0.1s
    => [12/17] COPY --chown=appusr:appgrp ./db ./db                                                                                0.1s
    => [13/17] COPY --chown=appusr:appgrp ./ext_api ./ext_api                                                                      0.1s
    => [14/17] COPY --chown=appusr:appgrp ./utils ./utils                                                                          0.1s
    => [15/17] COPY --chown=appusr:appgrp ./settings.py ./                                                                         0.1s
    => [16/17] COPY --chown=appusr:appgrp ./api_main.py ./                                                                         0.1s
    => [17/17] COPY --chown=appusr:appgrp ./tests/.env ./                                                                          0.1s
    => exporting to image                                                                                                          0.3s
    => => exporting layers                                                                                                         0.2s
    => => writing image sha256:061c8bd329befc32240d8873262cb9205cfedcd5bc0a4094bf109c2c4164eef5                                    0.0s
    => => naming to docker.io/library/tests-test_currency_api                                                                      0.0s
    02-Jan-2023 04:37:24PM [INFO] Docker: Startup initiated in detached mode
    02-Jan-2023 04:37:24PM [INFO] Engine Connection: Waiting for Database: (2013, 'Lost connection to MySQL server during query')
    02-Jan-2023 04:37:29PM [INFO] Engine Connection: Waiting for Database: (2013, 'Lost connection to MySQL server during query')
    02-Jan-2023 04:37:34PM [INFO] Engine Connection: Waiting for Database: (2013, 'Lost connection to MySQL server during query')
    02-Jan-2023 04:37:40PM [INFO] Database: Opening DB connection
    PASSED
    tests/test_api.py::test_api_currencies_rates PASSED
    tests/test_api.py::test_latest_rate_for_currency_success PASSED
    tests/test_api.py::test_currency_non_existant PASSED02-Jan-2023 04:37:51PM [INFO] Database: Test completed, DB connection closed

    tests/test_db.py::test_currency_codes 02-Jan-2023 04:37:51PM [INFO] Database: Opening DB connection
    PASSED
    tests/test_db.py::test_last_update PASSED
    tests/test_db.py::test_all_latest_rates_correct PASSED
    tests/test_db.py::test_latest_rate_correct PASSED
    tests/test_db.py::test_latest_rate_curr_non_existant PASSED
    tests/test_db.py::test_rate_on_date_correct PASSED
    tests/test_db.py::test_add_update_wrong_date_exception PASSED
    tests/test_db.py::test_get_rate_on_date_wrong_date_exception PASSED
    tests/test_db.py::test_currency_conversion PASSED02-Jan-2023 04:37:57PM [INFO] Database: Test completed, DB connection closed
    02-Jan-2023 04:37:57PM [INFO] Docker: Removing Containers
    02-Jan-2023 04:38:02PM [INFO] Docker: Removed


    ======================================================= 13 passed in 48.04s ========================================================
