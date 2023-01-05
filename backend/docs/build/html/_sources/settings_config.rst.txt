Settings Configuration
======================

Application settings are defined using Python's ``pydantic`` module, which are read from an ``.env`` file in the root directory.

An example settings file is provided as ``.env-template``. This should be copied to ``.env`` and updated as required in a production environment.

There are 3 groups of settings available in the ``.env`` file, with their respective prefixes :-

#. MySQL - ``MYSQL__*``
    Settings for MySQL server, like database name, port, user name, password etc.

#. Database updater - ``UPDATER__*``
    Settings for the database updater service. There is only one setting available: ``UPDATER__FREQUENCY``

#. Currency API - ``API__*``
    Settings related to the Currrency API.

    #. Startup - ``API__STARTUP__*``
        Settings related to the startup of the Currency API service.

    #. Authentication - ``API__AUTH__*``
        Settings related to cryptography for implementing authentication.

    #. User - ``API__USER__*``
        Details for the default user that is created when the Currency API server is started for the first time.
