import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health(ac: AsyncClient) -> None:
    response = await ac.get(
        "/",
    )
    assert 200 == response.status_code
