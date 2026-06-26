---
layout: default
class: code-center
---


# Start with plain dataclasses

<div class="divider-red"></div>

<p class="slide-tagline">No framework. Just data and rules.</p>

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
Start here. No database, no framework. Plain dataclasses with raw primitives.

Room enforces capacity inside add_reservation. That's the only business rule shown. Everything else is just data.
-->
