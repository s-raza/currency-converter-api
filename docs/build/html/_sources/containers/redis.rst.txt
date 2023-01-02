Redis Server
============

The Redis server running in this container caches API responses to avoid the overhead
of querying the MySQL database. This is implemented as a middleware in the
:doc:`Currency API service <currency_api>`, that connects to this Redis service for all its
caching needs.
