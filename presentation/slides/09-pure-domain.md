---
layout: default
class: code-center
---


# pure domain model

<div class="divider-red"></div>

<p class="slide-tagline">Raw primitives — business rules in class methods.</p>

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
Here is our initial pure domain model. Note that fields like room_id and capacity are typed as raw strings and integers.

The Room class aggregates its Reservations and enforces rules like capacity validation directly inside its add_reservation method. There is no infrastructure logic here.
-->
