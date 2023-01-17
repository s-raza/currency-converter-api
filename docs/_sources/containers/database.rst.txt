MySQL Database Server
=====================

When the system is deployed using docker-compose this container runs a MySQL
server that is responsible for receiving and saving the latest updates from
the :doc:`external source API </external_api>`.

These updates are perpetually retrieved at regular intervals by
the :doc:`Update Server <currency_updater>`.
