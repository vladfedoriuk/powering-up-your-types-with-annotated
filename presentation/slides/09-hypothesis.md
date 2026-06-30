---
layout: default
---


# Hypothesis: property-based testing

<div class="divider-red"></div>

<p class="slide-tagline"><code>st.builds</code> builds objects, <code>st.from_type</code> reads <code>Annotated</code> constraints.</p>

<div class="grid grid-cols-2 gap-x-4">

<div>

```python
@dataclass
class StayRequest:
    guest_count: GuestCount
    room_id: RoomId
    starts_at: date
    ends_at: date
```

</div>

<div>

```python
@given(
    req=st.builds(StayRequest),
    discount=st.from_type(Percentage),
    tax=st.from_type(TaxRate),
)
def test_stay_total(req, discount, tax):
    assume(req.starts_at <= req.ends_at)
    r = Reservation(
        room_id=req.room_id,
        guest_count=req.guest_count,
        starts_at=req.starts_at,
        ends_at=req.ends_at,
        rate=Decimal("100"),
    )
    assert calculate_stay_total(r, discount, tax) >= 0
```

</div>

</div>

<!--
st.builds(StayRequest) generates guest_count, room_id, starts_at, ends_at from their types — it reads Annotated constraints automatically. st.from_type(Percentage) and st.from_type(TaxRate) work the same way.
-->
