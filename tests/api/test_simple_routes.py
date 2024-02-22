from httpx import AsyncClient
import pytest


@pytest.mark.anyio
async def test_index(client: AsyncClient):
    response = await client.get("/")

    assert {"Hello": "World"} == response.json()
