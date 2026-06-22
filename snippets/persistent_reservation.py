import datetime
from decimal import Decimal
from typing import Annotated

import sqlalchemy.orm
from annotated_types import Ge, Gt, IsFinite, IsNotNan, Le, MaxLen, MinLen, Timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship

DATABASE_URL = "sqlite+aiosqlite:///reservation.db"

metadata = sqlalchemy.MetaData()
registry = sqlalchemy.orm.registry(metadata=metadata)

Identity = Annotated[
    int,
    Gt(0),
    mapped_column(
        sqlalchemy.Integer(),
        sqlalchemy.Identity(always=False),
        primary_key=True,
    ),
]

RoomId = Annotated[
    str,
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

Amount = Annotated[Decimal, IsFinite, IsNotNan]

RoomRate = Annotated[
    Amount,
    Gt(0),
    mapped_column(sqlalchemy.Numeric(precision=10, scale=2), nullable=False),
]

Percentage = Annotated[Amount, Ge(0), Le(100)]
TaxRate = Annotated[Amount, Ge(0), Le(1)]

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


@registry.mapped_as_dataclass
class Room:
    """Room aggregate root. Rules live here."""

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


@registry.mapped_as_dataclass
class Reservation:
    """Reservation entity inside a room aggregate."""

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
