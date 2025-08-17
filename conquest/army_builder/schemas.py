from typing import Self
from uuid import UUID, uuid4

from pydantic import Field, NonNegativeInt

from conquest.core.schemas import BaseModelConquest, EntrySlug, FactionSlug, GameSlug


class ArmyEntry(BaseModelConquest):
    """
    Represents an entry in the army, which can be a unit or an addon.
    """

    id: UUID = Field(default_factory=uuid4)
    entry_slug: EntrySlug
    type: str
    selections: list[str] = Field(default_factory=list, description="List of slugs for selected addons in this entry")
    linked_nodes: dict = Field(default_factory=dict, description="Linked nodes for the army builder UI")
    children: list[Self] = Field(default_factory=list, description="List of child entries for this army entry")


class Army(BaseModelConquest):
    """
    Represents an army in the Conquest game.
    """

    id: UUID = Field(default_factory=uuid4)
    name: str
    points: NonNegativeInt  # Total points of the army
    faction_slug: FactionSlug
    game_slug: GameSlug
    selections: list[
        str
    ] = []  # Field(default_factory=list, description="List of slugs for selected addons in the army")
    linked_nodes: dict = Field(default_factory=dict, description="Linked nodes for the army builder UI")
    saved: bool = Field(default=False, description="Indicates if the army is saved in the database")
    children: list[ArmyEntry]
