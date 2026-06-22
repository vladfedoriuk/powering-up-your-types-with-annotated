import datetime
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Reservation:
    room_id: str
    guest_count: int
    starts_at: datetime.date
    ends_at: datetime.date
    rate: Decimal
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )

    @property
    def night_count(self) -> int:
        return (self.ends_at - self.starts_at).days

    def overlaps(self, other: "Reservation") -> bool:
        return self.starts_at < other.ends_at and other.starts_at < self.ends_at


@dataclass
class Room:
    room_id: str
    capacity: int
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
