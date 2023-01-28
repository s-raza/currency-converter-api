Run Services using Docker
=========================

Starting the Services
---------------------

Using this method the services run inside docker containers. A `docker-compose.yml`
file is provided to orchestrate the services. Once the containers are up and running
the API endpoints are available at `http://localhost:8080` and the React frontend
is accessible from `http://localhost:3002`

Below are the steps for running the Currency converter API.

#. Install `Docker <https://docs.docker.com/get-docker/>`_

#. Clone this repository to your local machine.

  .. code-block:: bash

    git clone https://github.com/s-raza/currency-converter-api.git

#. Change to the `currency-converter-api` directory, which contains the `docker-compose.yml`
   file.

   .. code-block:: bash

    cd currency-converter-api

#. Copy the `.env-template` file to `.env`, all the settings in it can be left as they
   are for local testing purposes.

#. Run docker compose

   - To build and run the React frontend with Nginx. The React frontend will be accessible
     from `http://localhost:3002`, API endpoints will be available at `http://localhost:8080`

    .. code-block:: bash

      docker compose up prod-server --build -d

   - To run the frontend using the webpack dev server included with React. The React frontend
     will be accessible from `http://localhost:3002`, API endpoints will be available at `http://localhost:8080`

    .. code-block:: bash

        docker compose up dev-server --build -d

   - To run only the FastAPI backend. The endpoints will be available at `http://localhost:8080`

    .. code-block:: bash

        docker compose up api --build -d

   - To run only the updater that updates the MySQL database with the latest rates.

    .. code-block:: bash

        docker compose up updater --build -d

Stopping the Services
---------------------

To stop the containers run the below command from the same directory in which the `docker-compose.yml`
file is present.

.. code-block:: bash

    docker compose down
