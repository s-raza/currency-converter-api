Docker Containers
=================

The currency converter is implemented using different services running in docker
containers and orchestrated using :doc:`Docker Compose <usage/docker/index>` or
:doc:`Kubernetes <usage/k8s/index>`.

These containers co-ordinate to implement the over all functionality of the system.

.. _containers-updater:

Database Updater Service
------------------------

When the system is deployed using :doc:`Docker <usage/docker/index>` or
:doc:`Kubernetes <usage/k8s/index>` this container is responsible
for perpetually retrieving the latest currency rates from the
:doc:`External API Server <external_api>` and updating them in
`MySQL Database Service`_ that is running in a
different container.

The frequency of the updates is configurable using the ``UPDATER__FREQUENCY``
setting in the ``.env`` file.

Any API calls received by the `FastAPI Service`_ uses the latest or historical data
from the MySQL container.

.. _containers-database:

MySQL Database Service
----------------------

A container running MySQL server acts as the back end from which client
requests to the API are fulfilled.

This container runs a MySQL server that is responsible for receiving and
saving the latest updates from the :doc:`external source API <external_api>`.

These updates are perpetually retrieved at regular intervals by the
`Database Updater Service`_ and saved to the MySQL database running inside
this container.

.. _containers-fastapi:

FastAPI Service
---------------

This service exposes the :doc:`API end-points <api_endpoints>` for the currency converter.

.. _containers-redis:

Redis Caching Service
---------------------

This service caches the API responses in Redis to avoid the overhead of querying
the MySQL database. This is implemented as a middleware in the `FastAPI Service`_,
that connects to this Redis service for all its caching needs.

.. _containers-react:

React Frontend Service
----------------------

Frontend interface that consumes the :doc:`API end-points <api_endpoints>` from the backend
`FastAPI Service`_.

This container exposes the Web GUI for the currency converter using
React's built-in Webpack development server. This service consumes the backend
`FastAPI Service`_ to implement various features like a currency converter, table
with latest currency rates, etc.

The default login credentials are user:pass123

.. _containers-nginx:

NGINX Service
-------------

Frontend interface same as the `React Frontend Service`_
but exposed using a production build of the React application using NGINX.

This service exposes the Web GUI for the currency converter using NGINX.
Upon building its image the source files from the `React Frontend Service`_
are built and placed in the appropriate directory within the NGINX
container, ready to be served to a browser.

The default login credentials are user:pass123
