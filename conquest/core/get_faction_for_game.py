import httpx
from mcp.server.fastmcp import Context

from conquest.core.config import BASE_URL
from conquest.core.mcp import mcp
from conquest.core.schemas import Faction, FactionSlug, GameSlug


@mcp.tool()
async def get_faction_for_game(
    ctx: Context,
    faction_slug: FactionSlug,
    game_slug: GameSlug,
) -> Faction:
    """
    Get a list of units for a specific faction and game.
    """
    url = f"{BASE_URL}/{game_slug}/factions/{faction_slug}.json"
    async with httpx.AsyncClient() as client:
        try:
            await ctx.info(f"Fetching units for faction '{faction_slug}' in game '{game_slug}' from {url}")
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            # Log the response
            data = response.json()
            await ctx.info(
                f"Fetched {len(data.get('entries', []))} entries for faction '{faction_slug}' in game '{game_slug}'"
            )
            # Return the faction with its entries
            return Faction(**data)
        except Exception as e:
            await ctx.error(f"Error fetching units for faction '{faction_slug}' in game '{game_slug}': {e}")
            return Faction(slug=faction_slug, name="", entries={})
    return Faction(slug=faction_slug, name="", entries={})
