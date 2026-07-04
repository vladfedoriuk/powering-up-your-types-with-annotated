---
layout: default
class: code-center
---

# Using factories in tests

<div class="divider-red"></div>

```python {all|2|3-6|8-9}
def test_duplicate_reservation_is_rejected() -> None:
    reservation = ReservationFactory.build(room_id="101")
    room = RoomFactory.build(
        room_id="101",
        reservations=[reservation],
    )

    with pytest.raises(ValueError, match="Reservation overlaps existing reservation"):
        room.add_reservation(reservation)
```

<!--
Now we actually use the factory in a test.

[click] `ReservationFactory` spins up guest_count, rate, and room_id straight from the Annotated constraints.

[click] We hand that reservation to `RoomFactory` as its starting state

[click] then add the exact same reservation again — same `starts_at`, same `ends_at` — which trips the overlap check against itself.
-->
