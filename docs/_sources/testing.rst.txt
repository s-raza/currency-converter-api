Testing
=======

Tests are implemented using Python's pytest module and live MySQL
and API servers using docker.

The docker containers are started upon initiating tests using pytest and
all the tests are run against the live MySQL and API servers.

Example run:

.. code-block:: text

    currency-converter-api> cd backend
    currency-converter-api\backend> pytest -s -v

    platform win32 -- Python 3.9.0, pytest-7.2.0, pluggy-1.0.0 -- C:\.python_venvs\poetry\cache\virtualenvs\currency-converter-api-5abJ2n6c-py3.9\Scripts\python.exe
    cachedir: .pytest_cache
    rootdir: D:\Development\currency-converter-api\backend
    plugins: anyio-3.6.2, asyncio-0.19.0, cov-2.12.1, typeguard-2.13.3
    asyncio: mode=strict
    collected 13 items

    tests/test_api.py::test_api_currencies_list 17-Jan-2023 12:53:47PM [INFO] Docker: Starting Docker Containers
    failed to get console mode for stderr: The handle is invalid.
    [+] Building 3.8s (21/21) FINISHED
    => [internal] load build definition from Dockerfile.api                                                                        0.1s
    => => transferring dockerfile: 36B                                                                                             0.0s
    => [internal] load .dockerignore                                                                                               0.0s
    => => transferring context: 2B                                                                                                 0.0s
    => [internal] load metadata for docker.io/library/python:3.9.16-slim                                                           2.6s
    => [ 1/16] FROM docker.io/library/python:3.9.16-slim@sha256:0b19e7429c822572b27627a887470a9337e9477d4099bc9f79fb2cd5a5764278   0.0s
    => [internal] load build context                                                                                               0.1s
    => => transferring context: 215.91kB                                                                                           0.0s
    => CACHED [ 2/16] RUN apt-get update; apt-get install curl -y                                                                  0.0s
    => CACHED [ 3/16] RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry POETRY_VERSION=1.2.0 python &&     0.0s
    => CACHED [ 4/16] RUN groupadd -r appgrp                                                                                       0.0s
    => CACHED [ 5/16] RUN useradd -r -m appusr                                                                                     0.0s
    => CACHED [ 6/16] RUN usermod -a -G appgrp appusr                                                                              0.0s
    => CACHED [ 7/16] WORKDIR /app/.                                                                                               0.0s
    => CACHED [ 8/16] RUN chown appusr:appgrp /app/.                                                                               0.0s
    => CACHED [ 9/16] COPY --chown=appusr:appgrp ././pyproject.toml ././poetry.lock* ./                                            0.0s
    => CACHED [10/16] RUN poetry install --no-root --without dev                                                                   0.0s
    => [11/16] COPY --chown=appusr:appgrp ././currency_api ./currency_api                                                          0.1s
    => [12/16] COPY --chown=appusr:appgrp ././db ./db                                                                              0.1s
    => [13/16] COPY --chown=appusr:appgrp ././utils ./utils                                                                        0.1s
    => [14/16] COPY --chown=appusr:appgrp ././settings.py ./                                                                       0.1s
    => [15/16] COPY --chown=appusr:appgrp ././api_main.py ./                                                                       0.1s
    => [16/16] COPY --chown=appusr:appgrp ./tests/.env ./                                                                          0.1s
    => exporting to image                                                                                                          0.3s
    => => exporting layers                                                                                                         0.2s
    => => writing image sha256:dde26c9d46ebbe0cd680e283aeb03da77ab7ec7cb5d667218cf730464bcf2951                                    0.0s
    => => naming to docker.io/library/tests-test-currency-api                                                                      0.0s
    17-Jan-2023 12:54:16PM [INFO] Docker: Startup initiated in detached mode
    17-Jan-2023 12:54:18PM [INFO] Database: Opening DB connection
    17-Jan-2023 12:54:18PM [INFO] API Fixture: Waiting for API Server: http://localhost:8080/token
    17-Jan-2023 12:54:20PM [INFO] API Fixture: Waiting for API Server: http://localhost:8080/token
    17-Jan-2023 12:54:22PM [INFO] API Fixture: Waiting for API Server: http://localhost:8080/token
    17-Jan-2023 12:54:24PM [INFO] API Fixture: API server started
    PASSED
    tests/test_api.py::test_api_currencies_rates PASSED
    tests/test_api.py::test_latest_rate_for_currency_success PASSED
    tests/test_api.py::test_currency_non_existant PASSED17-Jan-2023 12:54:30PM [INFO] Database: Test completed, DB connection closed

    tests/test_db.py::test_currency_codes 17-Jan-2023 12:54:30PM [INFO] Database: Opening DB connection
    PASSED
    tests/test_db.py::test_last_update PASSED
    tests/test_db.py::test_all_latest_rates_correct PASSED
    tests/test_db.py::test_latest_rate_correct PASSED
    tests/test_db.py::test_latest_rate_curr_non_existant PASSED
    tests/test_db.py::test_rate_on_date_correct PASSED
    tests/test_db.py::test_add_update_wrong_date_exception PASSED
    tests/test_db.py::test_get_rate_on_date_wrong_date_exception PASSED
    tests/test_db.py::test_currency_conversion PASSED17-Jan-2023 12:54:36PM [INFO] Database: Test completed, DB connection closed
    17-Jan-2023 12:54:36PM [INFO] Docker: Removing Containers
    17-Jan-2023 12:54:41PM [INFO] Docker: Removed
