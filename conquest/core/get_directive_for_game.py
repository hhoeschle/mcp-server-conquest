import httpx
from mcp.server.fastmcp import Context

from conquest.core.config import BASE_URL
from conquest.core.mcp import mcp
from conquest.core.schemas import Directive, DirectiveSlug, GameSlug


@mcp.tool()
async def get_directive_for_game(
    ctx: Context,
    directive_slug: DirectiveSlug,
    game_slug: GameSlug,
) -> Directive:
    """
    Get details about a directive for a specific game.
    """
    url = f"{BASE_URL}/{game_slug}/directives/{directive_slug}.json"
    async with httpx.AsyncClient() as client:
        try:
            await ctx.info(f"Fetching rules for directive '{directive_slug}' in game '{game_slug}' from {url}")
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            # Log the response
            data = response.json()
            await ctx.info(f"Fetched directive '{directive_slug}' in game '{game_slug}'")
            # Return the directive with its entries
            return Directive(**data)
        except Exception as e:
            await ctx.error(f"Error fetching rules for directive '{directive_slug}' in game '{game_slug}': {e}")
            return Directive(slug=directive_slug, name="", description=None)
    return Directive(slug=directive_slug, name="", description=None)
