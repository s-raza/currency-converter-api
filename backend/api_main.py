from typing import Any

import aioredis
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import iterate_in_threadpool

from currency_api import utils
from currency_api.currencies_router import currencies_router
from currency_api.user_auth_router import user_router
from db.currency_db import CurrencyDB
from db.database import get_db
from db.utils import wait_for_db
from settings import settings as cfg

app = FastAPI()


@app.middleware("http")
async def redis_cache(request: Request, call_next: Any) -> Response:
    """
    Redis middleware implementation for caching responses.

    The value ``REDIS__EXPIRE_SECONDS`` from the `.env` file is used to set the expiry
    of a cached key, value pair that is cached using Redis.

    Once the number of seconds that are set pass, the entry is deleted from Redis cache,
    forcing a fresh query to the database upon the next request to the same endpoint
    with the same request path and query parameters.

    The caching is applied selectively only to the requests that have the value of
    ``API__PREFIX`` from ``.env`` file present in them. This is to avoid caching any
    other requests that are related to authentication and error responses.

    `Key`     : Combination of API request path and query parameters

    `Value`   : API response after querying the database.

    :param request: :obj:`fastapi.Request` object.
    :type request: required

    :param call_next: :obj:`Callable` callback for getting response from API endpoint.
    :type call_next: required

    :return: :obj:`fastapi.Response` object
    """

    url = utils.request_url(request)
    redis = aioredis.from_url(
        f"redis://{cfg().redis.host}:{cfg().redis.port}", decode_responses=True
    )

    if cfg().api.prefix in url:
        from_redis = await redis.execute_command("GET", url)

        if not from_redis:
            response: Response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))

            resp_str = response_body[0].decode()
            if response.status_code == 200:
                await redis.execute_command(
                    "SETEX", url, cfg().redis.expire_seconds, resp_str
                )
            else:
                await redis.execute_command("DEL", url)
            response_to_send = response
        else:
            response_to_send = Response(
                content=from_redis,
                status_code=200,
                media_type="application/json",
            )

        return response_to_send

    return await call_next(request)


origins = [
    f"https//{cfg().api.container.name}:{cfg().api.startup.port}",
    f"http//{cfg().api.container.name}:{cfg().api.startup.port}",
    f"https//{cfg().nginx.container.name}:{cfg().api.startup.port}",
    f"http//{cfg().nginx.container.name}:{cfg().api.startup.port}",
    f"https//localhost:{cfg().api.startup.port}",
    f"http//localhost:{cfg().api.startup.port}",
    f"https//127.0.0.1:{cfg().api.startup.port}",
    f"http//127.0.0.1:{cfg().api.startup.port}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(currencies_router, prefix=f"/{cfg().api.prefix}")
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
