from uuid import uuid4

from mcp.server.fastmcp import Context

from conquest.army_builder.schemas import ArmyEntry
from conquest.core.mcp import mcp
from conquest.core.schemas import Entry


@mcp.tool(
    name="Transfer Entry to ArmyEntry",
    structured_output=True,
)
async def get_army_entry(
    ctx: Context,
    entry: Entry,
) -> ArmyEntry:
    # Implementation to retrieve the army entry goes here
    await ctx.info(f"Creating army entry for {entry.slug}")
    army_entry = ArmyEntry(id=uuid4(), entry_slug=entry.slug, type="regiment")
    await ctx.info(f"Army entry created: {army_entry}")
    return army_entry
