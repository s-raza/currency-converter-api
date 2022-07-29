from typing import Any

import aioredis
import uvicorn
from fastapi import FastAPI, Request, Response
from starlette.concurrency import iterate_in_threadpool

from currency_api.currencies_router import currencies_router
from currency_api.middleware import utils
from currency_api.user_auth_router import user_router
from db.currency_db import CurrencyDB
from db.database import get_db
from db.utils import wait_for_db
from settings import settings as cfg

app = FastAPI()
currencies_prefix = "currencies"

redis = aioredis.from_url(
    f"redis://{cfg().redis.host}:{cfg().redis.port}", decode_responses=True
)


@app.middleware("http")
async def redis_cache(request: Request, call_next: Any) -> Response:

    url = utils.request_url(request)

    if currencies_prefix in url:
        from_redis = await redis.execute_command("GET", url)

        if not from_redis:
            response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))

            resp_str = response_body[0].decode()
            await redis.execute_command(
                "SETEX", url, cfg().redis.expire_seconds, resp_str
            )
            response_to_send = response
        else:
            response_to_send = Response(
                content=from_redis,
                status_code=200,
                media_type="application/json",
            )

        return response_to_send

    return await call_next(request)


app.include_router(currencies_router, prefix=f"/{currencies_prefix}")
app.include_router(user_router)


@app.on_event("startup")
async def add_default_user() -> None:
    """
    Ceates the default user on FastAPI startup.
    """

    db = await get_db(CurrencyDB)
    apiuser = cfg().api.user.dict()

    if not await db.get_user(apiuser["username"]):
        await db.add_user(**apiuser)


def main() -> None:
    """
    Main entry point for the FastAPI server.

    Waits for the database to startup before starting up itself.
    """

    wait_for_db(cfg().db_conn_settings, extra_sleep=5)
    config = cfg().api.startup
    uvicorn.run(
        config.uvicorn_entry,
        host="0.0.0.0",
        port=config.port,
        reload=config.uvicorn_reload,
    )


if __name__ == "__main__":
    main()
