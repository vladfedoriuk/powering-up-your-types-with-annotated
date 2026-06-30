---
layout: default
class: code-center
---


# Using factories in tests

<div class="divider-red"></div>

```python
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
ReservationFactory.build() auto-generates guest_count, rate, room_id from Annotated constraints. RoomFactory.build() takes that reservation as initial state via reservations=[...]. Adding the same reservation again triggers the overlap check — identical starts_at and ends_at means it overlaps itself.
-->
