import datetime
from collections.abc import AsyncGenerator
from decimal import Decimal
from typing import Annotated, Any, TypeAlias

import attr
import sqlalchemy
import sqlalchemy.orm
import svcs
import svcs.fastapi
from annotated_doc import Doc
from annotated_types import Ge, Gt, IsFinite, IsNotNan, Le, MaxLen, MinLen, Timezone
from attrs import frozen
from fastapi import FastAPI, HTTPException, Path, status
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
    model_validator,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)
from starlette.requests import Request
from starlette.responses import JSONResponse

DATABASE_URL = "sqlite+aiosqlite:///reservation.db"
engine = create_async_engine(DATABASE_URL)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as session:
        yield session


Identity = Annotated[
    int,
    Gt(0),
    mapped_column(
        sqlalchemy.Integer(),
        sqlalchemy.Identity(always=False),
        primary_key=True,
    ),
]


def trim_str(v: str) -> str:
    return v.strip()


RoomId = Annotated[
    str,
    BeforeValidator(trim_str),
    MinLen(1),
    MaxLen(20),
    mapped_column(sqlalchemy.String(20), nullable=False, index=True, unique=True),
]

GuestCount = Annotated[
    int,
    Ge(1),
    Le(10),
    mapped_column(sqlalchemy.Integer(), nullable=False),
]

NightCount = Annotated[int, Ge(1), Le(365)]


def serialize_amount(v: Decimal) -> float:
    return float(v.quantize(Decimal("0.01")))


Amount = Annotated[
    Decimal,
    IsFinite,
    IsNotNan,
    PlainSerializer(serialize_amount, return_type=float, when_used="json"),
]

RoomRate = Annotated[
    Amount,
    Gt(0),
    mapped_column(sqlalchemy.Numeric(precision=10, scale=2), nullable=False),
]

Percentage: TypeAlias = Annotated[Amount, Ge(0), Le(100)]
TaxRate: TypeAlias = Annotated[Amount, Ge(0), Le(1)]

StayDate = Annotated[
    datetime.date,
    mapped_column(sqlalchemy.Date(), nullable=False),
]

TimestampTz = Annotated[
    datetime.datetime,
    Timezone(...),
    mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.current_timestamp(),
    ),
]


class Base(DeclarativeBase, MappedAsDataclass):
    pass


metadata = Base.metadata


class Room(Base):
    __tablename__ = "rooms"
    __table_kwargs__ = {"sqlite_autoincrement": True}

    id: Mapped[Identity] = mapped_column(init=False)
    room_id: Mapped[RoomId]
    capacity: Mapped[GuestCount]
    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="room",
        default_factory=list,
    )

    def add_reservation(self, reservation: "Reservation") -> None:
        if reservation.room_id != self.room_id:
            raise ValueError("Reservation belongs to another room")
        if reservation.guest_count > self.capacity:
            raise ValueError("Reservation exceeds room capacity")
        if reservation.night_count < 1:
            raise ValueError("Reservation must last at least one night")
        if any(reservation.overlaps(existing) for existing in self.reservations):
            raise ValueError("Reservation overlaps existing reservation")
        reservation.room = self
        if reservation not in self.reservations:
            self.reservations.append(reservation)


class Reservation(Base):
    __tablename__ = "reservations"
    __table_kwargs__ = {"sqlite_autoincrement": True}

    id: Mapped[Identity] = mapped_column(init=False)
    room_id: Mapped[RoomId] = mapped_column(sqlalchemy.ForeignKey("rooms.room_id"))
    guest_count: Mapped[GuestCount]
    starts_at: Mapped[StayDate]
    ends_at: Mapped[StayDate]
    rate: Mapped[RoomRate]
    created_at: Mapped[TimestampTz] = mapped_column(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    room: Mapped[Room] = relationship(back_populates="reservations", default=None)

    @property
    def night_count(self) -> NightCount:
        return self.ends_at.toordinal() - self.starts_at.toordinal()

    def overlaps(self, other: "Reservation") -> bool:
        return self.starts_at < other.ends_at and other.starts_at < self.ends_at


def calculate_stay_total(
    reservation: Reservation,
    discount_percent: Percentage = Decimal(0),
    tax_rate: TaxRate = Decimal("0.1"),
) -> RoomRate:
    subtotal = reservation.rate * Decimal(reservation.night_count)
    discount_amount = subtotal * (discount_percent / Decimal(100))
    total = (subtotal - discount_amount) * (Decimal(1) + tax_rate)
    return total.quantize(Decimal("0.01"))


class ReservationSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
        extra="forbid",
        title="Reservation",
    )

    guest_count: GuestCount
    starts_at: StayDate
    ends_at: StayDate
    rate: RoomRate
    created_at: TimestampTz
    night_count: NightCount = Field(title="Nights")

    @model_validator(mode="after")
    def check_dates(self) -> "ReservationSchema":
        if self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be after starts_at")
        expected = self.ends_at.toordinal() - self.starts_at.toordinal()
        if self.night_count != expected:
            raise ValueError(
                f"night_count={self.night_count} does not match date range ({expected})"
            )
        return self


class CreateReservationSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, title="Create Reservation")

    room_id: RoomId
    guest_count: GuestCount
    starts_at: StayDate
    ends_at: StayDate
    rate: RoomRate

    @model_validator(mode="after")
    def check_dates(self) -> "CreateReservationSchema":
        if self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be after starts_at")
        return self


class RoomSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
        extra="forbid",
        title="Room",
    )

    room_id: RoomId
    capacity: GuestCount
    reservations: list[ReservationSchema]


class RoomResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", title="Room Detail")

    room: RoomSchema
    totals: list[RoomRate]


@svcs.fastapi.lifespan
async def lifespan(_app_: FastAPI, _registry_: svcs.Registry) -> AsyncGenerator[None]:
    _registry_.register_factory(AsyncSession, get_session)

    async def room_repo_factory(container: svcs.Container) -> RoomRepository:
        session = await container.aget(AsyncSession)
        return RoomRepository(session)

    _registry_.register_factory(RoomRepository, room_repo_factory)
    yield


app = FastAPI(
    title="Room Reservation API",
    lifespan=lifespan,
)


@attr.frozen
class RoomRepository:
    """Repository for room aggregates."""

    _session: AsyncSession

    async def save(self, room: Room) -> None:
        self._session.add(room)
        await self._session.flush()

    async def get_by_room_id(self, room_id: RoomId) -> Room | None:
        stmt = (
            sqlalchemy.select(Room)
            .where(Room.room_id == room_id)
            .options(sqlalchemy.orm.selectinload(Room.reservations))
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()


@frozen
class NotFoundError(Exception):
    """Exception raised when an entity is not found."""

    message: Annotated[str, Doc("The human-readable error message")]


@app.exception_handler(NotFoundError)
def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )


DIRECT_BOOKING_DISCOUNT: Annotated[
    Percentage,
    Doc("Discount for direct room reservations"),
] = Decimal(10)


@app.get("/rooms/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: Annotated[RoomId, Path()],
    services: svcs.fastapi.DepContainer,
) -> dict[str, Any]:
    repo = await services.aget(RoomRepository)
    if (room := await repo.get_by_room_id(room_id)) is None:
        raise NotFoundError("Room not found")

    return {
        "room": room,
        "totals": [
            calculate_stay_total(reservation) for reservation in room.reservations
        ],
    }


@app.post("/reservations/", status_code=status.HTTP_201_CREATED)
async def create_reservation(
    data: CreateReservationSchema,
    services: svcs.fastapi.DepContainer,
) -> dict[str, Any]:
    repo = await services.aget(RoomRepository)
    room = await repo.get_by_room_id(data.room_id)
    if room is None:
        raise NotFoundError("Room not found")

    reservation = Reservation(
        room_id=data.room_id,
        guest_count=data.guest_count,
        starts_at=data.starts_at,
        ends_at=data.ends_at,
        rate=data.rate,
    )

    try:
        room.add_reservation(reservation)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    await repo.save(room)

    return {
        "id": reservation.id,
        "room_id": data.room_id,
        "guest_count": data.guest_count,
        "starts_at": data.starts_at.isoformat(),
        "ends_at": data.ends_at.isoformat(),
        "rate": serialize_amount(data.rate),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
