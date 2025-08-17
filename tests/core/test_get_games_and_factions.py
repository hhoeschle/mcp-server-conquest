import httpx
import pytest

from conquest.core.config import BASE_URL
from conquest.core.schemas import Game


@pytest.mark.asyncio
async def test_get_games_and_factions():
    url = f"{BASE_URL}/games.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        games = [Game(**game) for game in data]

        assert data == [game.model_dump(by_alias=True, exclude_unset=True) for game in games], "Data mismatch for games"
