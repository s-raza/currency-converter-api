from typing import Any

import aioredis
from fastapi import FastAPI, Request, Response
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

from settings import cfg
from utils import requests


class RedisMiddleware(BaseHTTPMiddleware):
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

    :param app: :obj:`FastAPI` object, that is automatically passed by the
        FastAPI().add_middleware()
    :type app: required

    :param expire_seconds: :obj:`int` TTL for the `redis` key, loaded from
        `REDIS__EXPIRE_SECONDS` in the `.env` file.
    :type expire_seconds: required
    """

    def __init__(
        self,
        app: FastAPI,
        expire_seconds: int,
    ):
        super().__init__(app)
        self.expire_seconds = expire_seconds

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """
        :param request: :obj:`fastapi.Request` object.
        :type request: required

        :param call_next: :obj:`Callable` callback for getting response
            from API endpoint.
        :type call_next: required

        :return: :obj:`fastapi.Response` object
        """
        url = requests.request_url(request)
        redis = aioredis.from_url(
            f"redis://{cfg.redis.host}:{cfg.redis.port}", decode_responses=True
        )

        if cfg.api.prefix in url:
            from_redis = await redis.execute_command("GET", url)

            if not from_redis:
                response: Response = await call_next(request)
                response_body = [chunk async for chunk in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body))

                resp_str = response_body[0].decode()
                if response.status_code == 200:
                    await redis.execute_command(
                        "SETEX", url, self.expire_seconds, resp_str
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
