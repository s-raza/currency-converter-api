from typing import Any, Dict

from pydantic import BaseModel, BaseSettings


def get_conn_string(db_settings: Dict[str, Any]) -> str:
    """
    Construct and return the DB connection string from the provided settings `dict`

    :param db_settings: `dict` of setting_name:value pairs
    :type db_settings: required

    :return: `str` Connection string.
    """
    return (
        f'{db_settings["dialect"]}://{db_settings["user"]}:{db_settings["password"]}'
        f'@{db_settings["host"]}:{db_settings["port"]}/{db_settings["database"]}'
    )


class MYSQL(BaseModel):
    """
    DB connection settings sourced from `.env` file.
    """

    user: str
    password: str
    database: str
    dialect: str
    host: str = "localhost"
    port: str = "3306"


class Updater(BaseModel):
    """
    DB updater setttings sourced from `.env` file.
    """

    frequency: int


class CurrencyAPIStartup(BaseModel):
    """
    Currency API setttings sourced from `.env` file.
    """

    port: int
    uvicorn_entry: str
    uvicorn_reload: bool


class CurrencyAPIAuth(BaseModel):
    """
    Currency API setttings sourced from `.env` file.
    """

    secret_key: str
    algorithm: str
    token_expire_minutes: int


class CurrencyAPIUser(BaseModel):
    """
    Currency API setttings sourced from `.env` file.
    """

    username = "user"
    email = "user@email.com"
    full_name = "User Full Name"
    disabled = False
    password = "pass123"


class CurrencyAPI(BaseModel):
    """
    Currency API setttings sourced from `.env` file.
    """

    startup: CurrencyAPIStartup
    auth: CurrencyAPIAuth
    user: CurrencyAPIUser


class Settings(BaseSettings):
    """
    Retrieve settings from the `.env` file.
    """

    mysql: MYSQL
    updater: Updater
    api: CurrencyAPI

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"

    @property
    def db_conn_str(self) -> str:
        """
        Generate and get DB connection string with settings from `.env` file.

        :return: `str` Connection string.
        """
        db = self.dict()["mysql"]
        return get_conn_string(db)

    @property
    def db_conn_settings(self) -> Dict[str, Any]:
        """
        Generate and get DB connection settings from `.env` file.

        :return: `dict` with setting_name:value pairs for the Database
        """
        return self.dict()["mysql"]


settings = Settings()