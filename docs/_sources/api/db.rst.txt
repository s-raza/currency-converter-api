MySQL Database
==============

**SQLAlchemy** ORM Models
-------------------------

Currencies
++++++++++

.. autoclass:: db.models.Currencies
    :show-inheritance:
    :members:
    :inherited-members:

CurrencyUpdateDates
+++++++++++++++++++

.. autoclass:: db.models.CurrencyUpdateDates
    :show-inheritance:
    :members:
    :inherited-members:

CurrencyUpdates
+++++++++++++++

.. autoclass:: db.models.CurrencyUpdates
    :show-inheritance:
    :members:
    :inherited-members:

User
++++

.. autoclass:: db.models.User
    :show-inheritance:
    :members:
    :inherited-members:

Currency Database Interface using **SQLAlchemy** ORM
----------------------------------------------------

.. autoclass:: db.currency_db.CurrencyDB
    :show-inheritance:
    :members:
    :inherited-members:

Database Engine and Sessions
----------------------------------------------------

get_engine
++++++++++

.. autofunction:: db.database.get_engine

create_all
++++++++++

.. autofunction:: db.database.create_all

get_async_session
+++++++++++++++++

.. autofunction:: db.database.get_async_session

get_db
++++++

.. autofunction:: db.database.get_db

Utils
-----

wait_for_db
+++++++++++

.. autofunction:: db.utils.wait_for_db
