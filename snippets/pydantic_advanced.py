from dataclasses import dataclass
from typing import Annotated, Any, TypeVar

from annotated_types import Gt, Len, MaxLen, MinLen
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    Field,
    GetPydanticSchema,
    PlainValidator,
    TypeAdapter,
    WithJsonSchema,
    WrapValidator,
)
from pydantic_core import CoreSchema, core_schema

PositiveInt = Annotated[int, Gt(0)]
type NamedPositiveInt = Annotated[int, Gt(0)]

T = TypeVar("T")
type ShortList[T] = Annotated[list[T], Len(max_length=4)]

type ConstrainedStr = Annotated[str, MinLen(1), MaxLen(100)]

TrimmedStr = Annotated[str, BeforeValidator(str.strip)]


def _shout(s: str) -> str:
    if not s.endswith("!"):
        raise ValueError
    return s


ShoutStr = Annotated[str, AfterValidator(_shout)]

HexInt = Annotated[
    int, PlainValidator(lambda v: int(v) if isinstance(v, int) else int(v, 16))
]

LoggedInt = Annotated[int, WrapValidator(lambda v, handler: handler(v))]

PosWithSchema = Annotated[int, Gt(0), WithJsonSchema({"type": "integer", "minimum": 1})]


@dataclass(frozen=True)
class Upper:
    def __get_pydantic_core_schema__(self, _source: Any, handler: Any) -> CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            lambda v, h: h(v).upper(), handler(_source)
        )


UpperStr = Annotated[str, Upper()]

NonEmptyStr = Annotated[
    str, GetPydanticSchema(lambda _s, h: core_schema.str_schema(min_length=1))
]

ta_pos = TypeAdapter(PositiveInt)
ta_hex = TypeAdapter(HexInt)
ta_short: TypeAdapter[ShortList[int]] = TypeAdapter(ShortList[int])


class AliasDemo(BaseModel):
    implicit: PositiveInt
    named: NamedPositiveInt


class GenericAlias(BaseModel):
    names: ShortList[str]


class ValidatedModel(BaseModel):
    trimmed: TrimmedStr
    shout: ShoutStr
    hex_int: HexInt
    logged: LoggedInt
    upper: UpperStr
    nonempty: NonEmptyStr
    pos_schema: PosWithSchema = Field(default=1)
