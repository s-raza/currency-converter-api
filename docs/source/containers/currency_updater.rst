Update Server
=============

When the system is deployed using `docker-compose` this container is responsible
for perpetually retrieving the latest currency rates from the :doc:`External API Server </external_api>`
and updating them in :doc:`MySQL Database Server <database>` that is running in a
different container.

The frequency of the updates is confifgurable using the ``UPDATER__FREQUENCY``
setting in the ``.env`` file.

Any API calls received by the Currency API uses the latest or historical data
from the MySQL container.
