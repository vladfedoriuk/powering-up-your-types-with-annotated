from __future__ import annotations

import datetime
import uuid
from decimal import Decimal
from typing import Annotated, TypeVar

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

# Variant A: Annotated as type_annotation_map keys. SQLAlchemy ignores metadata
# contents here; each Annotated alias object is a distinct lookup key.
ShortText = Annotated[str, "short_text"]
LongText = Annotated[str, "long_text"]
Money = Annotated[Decimal, "money"]
Rate = Annotated[Decimal, "rate"]

type ShortTextAlias = Annotated[str, "short_text_alias"]
type MoneyAlias = Annotated[Decimal, "money_alias"]

mapper_registry = registry(
    type_annotation_map={
        ShortText: sa.String(40),
        LongText: sa.String(500),
        Money: sa.Numeric(10, 2),
        Rate: sa.Numeric(5, 4),
        ShortTextAlias: sa.String(40),
        MoneyAlias: sa.Numeric(10, 2),
    }
)


class TypeMapBase(DeclarativeBase):
    registry = mapper_registry


class ReservationQuote(TypeMapBase):
    __tablename__ = "reservation_quotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_name: Mapped[ShortText]
    notes: Mapped[LongText]
    nightly_rate: Mapped[Money]
    tax_rate: Mapped[Rate]
    alias_name: Mapped[ShortTextAlias]
    alias_rate: Mapped[MoneyAlias]


# Variant B: Whole mapped_column() embedded in Annotated. This is the canonical
# reusable column blueprint form for repeated model attributes.
# Only type-level config lives in the alias — table-specific constraints
# (unique, index) go on the model field where they actually apply.
RoomIdColumn = Annotated[str, mapped_column(sa.String(20))]
CreatedAtColumn = Annotated[
    datetime.datetime,
    mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()
    ),
]

type RoomRateColumn = Annotated[
    Decimal,
    mapped_column(sa.Numeric(10, 2), nullable=False),
]


class BlueprintBase(DeclarativeBase):
    pass


class RoomTable(BlueprintBase):
    __tablename__ = "rooms_blueprint"

    id: Mapped[int] = mapped_column(primary_key=True)
    # unique=True, index=True are table-specific — not part of the type alias
    room_id: Mapped[RoomIdColumn] = mapped_column(unique=True, index=True)
    rate: Mapped[RoomRateColumn]
    created_at: Mapped[CreatedAtColumn]


# Variant C: Generic Annotated blueprint. SQLAlchemy 2.0.44+ supports applying
# one mapped_column() recipe to multiple Python types.
T = TypeVar("T")
PrimaryKey = Annotated[T, mapped_column(primary_key=True)]

type PrimaryKeyAlias[T] = Annotated[T, mapped_column(primary_key=True)]


class GenericBase(DeclarativeBase):
    pass


class IntKeyRoom(GenericBase):
    __tablename__ = "int_key_rooms"

    id: Mapped[PrimaryKey[int]]
    room_id: Mapped[str]


class UuidKeyRoom(GenericBase):
    __tablename__ = "uuid_key_rooms"

    id: Mapped[PrimaryKeyAlias[uuid.UUID]]
    room_id: Mapped[str]
