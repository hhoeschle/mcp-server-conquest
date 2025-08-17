from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, PositiveInt
from pydantic.alias_generators import to_camel


class BaseModelConquest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


FactionSlug = Annotated[str, Field(description="The unique identifier for the faction.")]


class Faction(BaseModelConquest):
    slug: FactionSlug
    name: str
    entries: dict[str, "Entry"] = {}


GameSlug = Annotated[
    Literal["tlaok", "fb"],
    Field(description="The unique identifier for the game, either 'tlaok' or 'fb'."),
]


class Game(BaseModelConquest):
    slug: GameSlug
    name: Literal["The Last Argument of Kings", "First Blood"]
    factions: list[Faction]


class StatLine(BaseModelConquest):
    march: PositiveInt | Literal["-"] = Field(alias="M", description="March value of the unit.")
    clash: PositiveInt = Field(alias="C", description="Clash value of the unit.")
    volley: NonNegativeInt | Literal["-"] = Field(alias="V", description="Volley value of the unit.")
    attack: PositiveInt = Field(alias="A", description="Attack value of the unit.")
    defense: NonNegativeInt | Literal["-"] = Field(alias="D", description="Defense value of the unit.")
    wounds: PositiveInt | Literal["-"] = Field(alias="W", description="Wounds value of the unit.")
    resolve: PositiveInt | Literal["-"] = Field(alias="R", description="Resolve value of the unit.")
    evasion: NonNegativeInt | Literal["-"] = Field(alias="E", description="Evasion value of the unit.")


class Profile(BaseModelConquest):
    profile_name: str
    statline: StatLine


DirectiveSlug = Annotated[str, Field(description="The unique identifier for the directive.")]


class Directive(BaseModelConquest):
    slug: DirectiveSlug
    name: str
    description: str | None = None


TagQueryRequestSlug = Annotated[str, Field(description="The unique identifier for the tag query request.")]


class TagQueryRequest(BaseModelConquest):
    slug: TagQueryRequestSlug
    type: Literal["directives"]


TagQueryLabel = Annotated[str, Field(description="The unique identifier for the tag query.")]


class TagQuery(BaseModelConquest):
    label: TagQueryLabel
    request: TagQueryRequest


TagSlug = Annotated[str, Field(description="The unique identifier for the tag.")]


class Tag(BaseModelConquest):
    name: str
    slug: TagSlug
    query: TagQuery | None = None


TagGroupSlug = Annotated[str, Field(description="The unique identifier for the tag group.")]


class TagGroup(BaseModelConquest):
    name: str
    slug: TagGroupSlug
    tags: list[Tag] | None = None


EntrySlug = Annotated[str, Field(description="The unique identifier for the entry within a faction.")]


class Entry(BaseModelConquest):
    slug: EntrySlug
    cost: NonNegativeInt | Literal["*", "Preview"]
    game_class: Literal["Light", "Medium", "Brute", "Heavy"] | None = None
    size: NonNegativeInt
    min_size: NonNegativeInt
    max_size: PositiveInt
    name: str
    statline: StatLine | None = None
    profiles: list[Profile] | None = None
    type: Literal["Infantry", "Brute", "Cavalry", "Monster", "Chariot"]
    tag_groups: list[TagGroup] | None = None
