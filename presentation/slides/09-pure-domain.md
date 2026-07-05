---
layout: default
class: code-center
---


# Room Reservation

<div class="divider-red"></div>

```python
@dataclass
class Reservation:
    room_id: str
    guest_count: int
    starts_at: datetime.date
    ends_at: datetime.date
    rate: Decimal

@dataclass
class Room:
    room_id: str
    capacity: int
    reservations: list[Reservation] = field(default_factory=list)

    def add_reservation(self, reservation: Reservation) -> None:
        if reservation.guest_count > self.capacity:
            raise ValueError("Exceeds room capacity")
        ...
```

<!--
We start with simple Python dataclasses. No databases or frameworks yet.

We have a `Reservation` and a `Room`. The `Room` checks rules like room capacity and date overlaps when we add a new reservation.

Right now, everything uses plain primitives like `str`, `int`, and `Decimal`. Let's change that.
-->
