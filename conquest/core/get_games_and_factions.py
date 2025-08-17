import httpx
from mcp.server.fastmcp import Context

from conquest.core.config import BASE_URL
from conquest.core.mcp import mcp
from conquest.core.schemas import Game


@mcp.tool()
async def get_games_and_factions(
    ctx: Context,
) -> list[Game]:
    """
    Get a list of games and available factions in each game.
    """
    url = f"{BASE_URL}/games.json"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            # Log the response
            return [Game(**game) for game in response.json()]
        except Exception as e:
            await ctx.error(f"Error fetching games and factions: {e}")
            return []
    return []
