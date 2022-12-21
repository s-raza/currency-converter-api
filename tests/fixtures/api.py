from asyncio import sleep

import pytest_asyncio
from httpx import AsyncClient, Auth, RemoteProtocolError, Response

from settings import settings as cfg


class PasswordAuth(Auth):
    def __init__(self, token):
        self.token = f"Bearer {token}"

    def auth_flow(self, request):
        request.headers["Authorization"] = self.token
        yield request


@pytest_asyncio.fixture(scope="module")
async def api():

    port = cfg().api.startup.port
    base_url = f"http://localhost:{port}"
    user_settings = cfg().api.user
    auth_client = AsyncClient(base_url=base_url, timeout=None)

    api_started = False

    while not api_started:
        try:
            token: Response = await auth_client.post(
                f"{base_url}/token",
                data={
                    "username": user_settings.username,
                    "password": user_settings.password,
                },
            )
            await auth_client.aclose()
            api_started = True
        except RemoteProtocolError:
            await sleep(1)
            continue

    auth = PasswordAuth(token.json()["access_token"])
    client = AsyncClient(
        base_url=f"{base_url}/{cfg().api.prefix}",
        auth=auth,
        timeout=None,
        follow_redirects=True,
    )

    yield client
    await client.aclose()
