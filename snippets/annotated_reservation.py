import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Annotated

from annotated_types import (
    Ge,
    Gt,
    Le,
    MaxLen,
    MinLen,
    Predicate,
    Timezone,
)

# Semantic Types
RoomId = Annotated[str, MinLen(1), MaxLen(20)]
GuestCount = Annotated[int, Ge(1), Le(10)]
NightCount = Annotated[int, Ge(1), Le(365)]

# The Base Layer: Amount must be a finite, non-NaN decimal.
Amount = Annotated[
    Decimal,
    Predicate(lambda x: x.is_finite()),
    Predicate(lambda x: not x.is_nan()),
]

# Layering: Adding domain constraints on top of the base Amount.
RoomRate = Annotated[Amount, Gt(0)]
Percentage = Annotated[Amount, Ge(0), Le(100)]
TaxRate = Annotated[Amount, Ge(0), Le(1)]
TimestampTz = Annotated[datetime.datetime, Timezone(...)]


@dataclass
class Reservation:
    room_id: RoomId
    guest_count: GuestCount
    starts_at: datetime.date
    ends_at: datetime.date
    rate: RoomRate
    created_at: TimestampTz = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )

    @property
    def night_count(self) -> NightCount:
        return self.ends_at.toordinal() - self.starts_at.toordinal()

    def overlaps(self, other: "Reservation") -> bool:
        return self.starts_at < other.ends_at and other.starts_at < self.ends_at


@dataclass
class Room:
    room_id: RoomId
    capacity: GuestCount
    reservations: list[Reservation] = field(default_factory=list)

    def add_reservation(self, reservation: Reservation) -> None:
        if reservation.room_id != self.room_id:
            raise ValueError("Reservation belongs to another room")
        if reservation.guest_count > self.capacity:
            raise ValueError("Reservation exceeds room capacity")
        if reservation.night_count < 1:
            raise ValueError("Reservation must last at least one night")
        if any(reservation.overlaps(existing) for existing in self.reservations):
            raise ValueError("Reservation overlaps existing reservation")
        self.reservations.append(reservation)


def calculate_stay_total(
    reservation: Reservation,
    discount_percent: Percentage = Decimal(0),
    tax_rate: TaxRate = Decimal("0.1"),
) -> RoomRate:
    """Rate x nights, then discount percentage and tax factor."""
    subtotal = reservation.rate * Decimal(reservation.night_count)
    discount_amount = subtotal * (discount_percent / Decimal(100))
    total = (subtotal - discount_amount) * (Decimal(1) + tax_rate)
    return total.quantize(Decimal("0.01"))
