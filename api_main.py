import uvicorn
from fastapi import FastAPI

from currency_api.currencies_router import currencies_router
from currency_api.user_auth_router import user_router
from db.currency_db import CurrencyDB
from db.database import get_db
from db.utils import wait_for_db
from settings import settings as cfg

app = FastAPI()
app.include_router(currencies_router)
app.include_router(user_router)


@app.on_event("startup")
async def add_default_user() -> None:

    db = await get_db(CurrencyDB)
    apiuser = cfg.api.user.dict()

    if not await db.get_user(apiuser["username"]):
        await db.add_user(**apiuser)


if __name__ == "__main__":

    wait_for_db(cfg.db_conn_settings, extra_sleep=5)
    config = cfg.api.startup
    uvicorn.run(
        config.uvicorn_entry,
        host="0.0.0.0",
        port=config.port,
        reload=config.uvicorn_reload,
    )
