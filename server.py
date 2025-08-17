from conquest.army_builder.create_army_builder_json import create_army_builder_json

# from conquest.army_builder.get_army_entry import get_army_entry
from conquest.core.get_directive_for_game import get_directive_for_game
from conquest.core.get_faction_for_game import get_faction_for_game
from conquest.core.get_games_and_factions import get_games_and_factions
from conquest.core.mcp import mcp

assert [
    get_directive_for_game,
    get_games_and_factions,
    get_faction_for_game,
    create_army_builder_json,
    # get_army_entry,
]

assert mcp is not None, "MCP server must be initialized before use"

if __name__ == "__main__":
    # Initialize and run the server
    print("Starting FastMCP server...")
    mcp.run(transport="stdio")
