from typing import Literal

import httpx
from mcp.server.fastmcp import Context

from conquest.core.config import BASE_URL
from conquest.core.mcp import mcp
from conquest.core.schemas import FactionOption, GameSlug


@mcp.tool()
async def get_faction_options_for_game(
    ctx: Context,
    faction_option: Literal["artefacts"],
    game_slug: GameSlug,
) -> FactionOption:
    """
    Get details about a faction options for a specific game.
    """
    url = f"{BASE_URL}/{game_slug}/faction-options/{faction_option}.json"

    async with httpx.AsyncClient() as client:
        try:
            await ctx.info(f"Fetching rules for faction option '{faction_option}' in game '{game_slug}' from {url}")
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            # Log the response
            data = response.json()
            await ctx.info(f"Fetched faction option '{faction_option}' in game '{game_slug}'")
            # Return the faction option with its entries
            return FactionOption(**data)
        except Exception as e:
            await ctx.error(f"Error fetching rules for faction option '{faction_option}' in game '{game_slug}': {e}")
            return FactionOption(slug=faction_option, name="", groups=None)
    return FactionOption(slug=faction_option, name="", groups=None)
