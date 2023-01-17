Settings Configuration
======================

Application settings are defined using Python's ``pydantic`` module,
which are read from an ``.env`` file in the root directory.

An example settings file is provided as ``.env-template``.
This should be copied to ``.env`` and updated as required in a production
environment.

The settings for each service are identified by their respective prefixes:-

#. MySQL - ``MYSQL__*``
#. Database updater - ``UPDATER__*``
#. Currency API - ``API__*``
    #. Startup - ``API__STARTUP__*``
    #. Authentication - ``API__AUTH__*``
    #. User - ``API__USER__*``
#. Redis cache - ``REDIS__*``
#. React application settings - ``REACT_APP__*``
#. NGINX ``NGINX__*``
#. Container settings - ``*__CONTAINER__*``
    Settings used within the `docker-compose.yml` file for various settings
    related to each service's container.

The settings can be accessed from within the code by importing the ``cfg``
variable from the ``settings`` module in other modules.

To use the settings in modules, for each directive replace the double underscore: ``__``
with a period ``.``

For example to use the ``API__USER__*`` setting to access the user settings:

.. code-block:: python

    from settings import cfg

    user_details = cfg.api.user

    print(user_details.username)
    print(user_details.email)
    print(user_details.full_name)

``API__STARTUP__UVICORN_ENTRY``

.. code-block:: python

    from settings import cfg
    print(cfg.api.startup.uvicorn_entry)
