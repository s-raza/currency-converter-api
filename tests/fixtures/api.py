import pytest_asyncio
from httpx import AsyncClient, Auth, Response


class PasswordAuth(Auth):
    def __init__(self, token):
        self.token = f"Bearer {token}"

    def auth_flow(self, request):
        request.headers["Authorization"] = self.token
        yield request


@pytest_asyncio.fixture(scope="module")
async def api():

    base_url = "http://localhost:8070"
    auth_client = AsyncClient(base_url=base_url)
    token: Response = await auth_client.post(
        f"{base_url}/token", data={"username": "user", "password": "pass123"}
    )
    await auth_client.aclose()

    auth = PasswordAuth(token.json()["access_token"])

    client = AsyncClient(base_url=f"{base_url}/currencies", auth=auth)
    yield client
    await client.aclose()
