import logging

import httpx
import pytest

from conquest.core.config import BASE_URL
from conquest.core.schemas import Faction, FactionSlug, GameSlug

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "game_slug,faction_slug",
    [
        (gs, fs)
        for gs in ["tlaok", "fb"]
        for fs in [
            "dweghom",
            "nords",
            "sorcerer-kings",
            "the-city-states",
            "the-hundred-kingdoms",
            "the-old-dominion",
            "the-spires",
            "the-wadrhun",
            "yoroni",
        ]
    ],
)
@pytest.mark.asyncio
async def test_get_faction_for_game(
    game_slug: GameSlug,
    faction_slug: FactionSlug,
):
    url = f"{BASE_URL}/{game_slug}/factions/{faction_slug}.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        faction = Faction(**data)
        logger.info(f"Retrieved faction for game '{game_slug}': {faction}")

        assert data == faction.model_dump(by_alias=True, exclude_unset=True), (
            f"Data mismatch for faction '{faction_slug}' in game '{game_slug}'"
        )
