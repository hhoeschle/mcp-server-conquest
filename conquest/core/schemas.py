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
    queries: list["Query"] | None = None
    entry_groups: list["EntryGroup"] = []


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
    command_range: PositiveInt | Literal["-"] | None = Field(
        alias="CR", description="Command range value of the unit.", default=None
    )
    volley: NonNegativeInt | Literal["-"] = Field(alias="V", description="Volley value of the unit.")
    attack: PositiveInt = Field(alias="A", description="Attack value of the unit.")
    defense: NonNegativeInt | Literal["-"] = Field(alias="D", description="Defense value of the unit.")
    wounds: PositiveInt | Literal["-"] = Field(alias="W", description="Wounds value of the unit.")
    resolve: PositiveInt | Literal["-"] = Field(alias="R", description="Resolve value of the unit.")
    evasion: NonNegativeInt | Literal["-"] = Field(alias="E", description="Evasion value of the unit.")


class Profile(BaseModelConquest):
    name: str | None = None
    profile_name: str
    statline: StatLine
    tag_groups: list["TagGroup"] | None = None


DirectiveSlug = Annotated[str, Field(description="The unique identifier for the directive.")]


class Directive(BaseModelConquest):
    slug: DirectiveSlug
    name: str
    description: str | None = None


QueryRequestSlug = Annotated[str, Field(description="The unique identifier for the query request.")]


class QueryRequest(BaseModelConquest):
    slug: QueryRequestSlug
    type: Literal["directives", "faction-options"]


QueryLabel = Annotated[str, Field(description="The unique identifier for the query.")]


class Query(BaseModelConquest):
    label: QueryLabel
    request: QueryRequest


TagSlug = Annotated[str, Field(description="The unique identifier for the tag.")]


class Tag(BaseModelConquest):
    name: str
    slug: TagSlug
    query: Query | None = None
    variable: PositiveInt | None = None
    range: PositiveInt | None = None
    tags: list["Tag"] | None = None


TagGroupSlug = Annotated[str, Field(description="The unique identifier for the tag group.")]


class TagGroup(BaseModelConquest):
    name: str
    slug: TagGroupSlug
    tags: list[Tag] | None = None


class RuleTarget(BaseModelConquest):
    type: Literal["SELF", "WARBAND", "LIST", "REGIMENT", "ALL_REGIMENTS", "REGIMENTS"]


class Rule(BaseModelConquest):
    type: Literal[
        "CHARACTER",
        "WARBAND_CONSTITUTION",
        "WARBAND",
        "STANDARD_BEARER",
        "OMNIPOTENCE",
        "FINEST_CAVALRY",
        "ONLY_ONE_OF",
        "BIOTIC_HIVE",
        "RUTHLESS_SOVEREIGNS",
        "SCION_OF_DEATH_WARBAND",
        "SCION_OF_WAR_WARBAND",
        "THUNDER_CHIEFTAIN_WARBAND",
        "MODULAR_REGIMENT",
        "LEADER_THRESHOLD",
        "BOUND_ELEMENTALS",
    ]
    targets: RuleTarget
    params: dict[str, str | int | float | bool] | None = None


class EffectParams(BaseModelConquest):
    tags: list[Tag] | list[str] | str | None = None
    tag_group: TagGroup | str | None = None
    key: Literal["CR", "M", "W", "A", "D", "R", "E", "C"] | None = None
    operation: Literal["add"] | None = None
    variable: NonNegativeInt | dict | None = None


class Effect(BaseModelConquest):
    type: Literal[
        "MODIFY_TAG",
        "ADD_TAGS",
        "MODIFY_STAT",
        "MODIFY_OPTION_GROUP",
        "MODIFY_OPTION_COST",
        "BERGONT_RAEGH",
        "HELLBRINGER_SORCERER",
        "FERRIC_THRONE",
        "REMOVE_TAGS",
    ]
    targets: RuleTarget | None = None
    params: EffectParams | None = None


OptionGroupSlug = Annotated[str, Field(description="The unique identifier for the option group.")]


class OptionGroup(BaseModelConquest):
    slug: OptionGroupSlug | None = None
    description: str | None = None
    name: str
    min_options: NonNegativeInt | None = None
    max_options: PositiveInt | None = None
    active: bool | None = None
    groups: list["OptionGroup"] | None = None
    query: Query | None = None
    orphans: list["OptionOrphan"] | None = None


class OptionOrphan(BaseModelConquest):
    slug: str | None = None
    name: str | None = None
    cost: NonNegativeInt | None = None
    active: bool | None = None
    query: Query | None = None
    effects: list[Effect] | None = None


class Options(BaseModelConquest):
    groups: list[OptionGroup] | None = None
    orphanes: list[OptionOrphan] | None = None


class Text(BaseModelConquest):
    content: str
    tag: str | None = None


EntrySlug = Annotated[str, Field(description="The unique identifier for the entry within a faction.")]


class Entry(BaseModelConquest):
    slug: EntrySlug
    cost: NonNegativeInt | Literal["*", "Preview"]
    game_class: Literal["Light", "Medium", "Brute", "Heavy"] | None = None
    size: NonNegativeInt
    size_step: NonNegativeInt | None = None
    size_step_cost: NonNegativeInt | None = None
    min_size: NonNegativeInt
    max_size: PositiveInt
    name: str
    statline: StatLine | None = None
    profiles: list[Profile] | None = None
    type: Literal["Infantry", "Brute", "Cavalry", "Monster", "Chariot"]
    texts: list[Text] | None = None
    tag_groups: list[TagGroup] | None = None
    rules: list[Rule] | None = None
    options: Options | None = None


EntryGroupSlug = Annotated[str, Field(description="The unique identifier for the entry group.")]


class EntryGroup(BaseModelConquest):
    entry_slugs: list[EntrySlug] = Field(default_factory=list, description="List of entry slugs in this group.")
    name: str = Field(description="Name of the entry group.")
    slug: EntryGroupSlug


class FactionOption(BaseModelConquest):
    slug: str
    name: str
    groups: list[TagGroup] | None = None
