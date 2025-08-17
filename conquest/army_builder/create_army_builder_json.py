from uuid import uuid4

from mcp.server.fastmcp import Context
from pydantic import Field, NonNegativeInt

from conquest.army_builder.schemas import Army, ArmyEntry
from conquest.core.mcp import mcp
from conquest.core.schemas import FactionSlug, GameSlug


@mcp.tool(
    structured_output=True,
)
async def create_army_builder_json(
    ctx: Context,
    game_slug: GameSlug,
    faction_slug: FactionSlug,
    army_name: str = Field(..., description="Name of the army"),
    army_points: NonNegativeInt = Field(..., description="Total points of the army"),
) -> Army:
    """
    Create a new army builder JSON object.
    This function initializes an empty army with default values.
    """
    await ctx.info("Creating a new army builder JSON object")

    army = Army(
        name=army_name,
        points=army_points,
        faction_slug=faction_slug,
        game_slug=game_slug,
        children=list[ArmyEntry](),  # Initialize with an empty list of entries
        linked_nodes={},
        saved=False,
        selections=list[str](),
        id=uuid4(),  # Generate a unique ID for the army
    )

    await ctx.info("New army builder JSON object created successfully")
    return army
