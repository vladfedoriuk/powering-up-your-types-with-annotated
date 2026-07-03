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

```python {all|2|3-4|all}
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
st.builds reads a dataclass's fields and works out how to generate each one — no manual strategy needed, same automatic reading polyfactory did with Annotated constraints.

[click] Here, it generates guest_count, room_id, starts_at, and ends_at straight from their types.

[click] st.from_type(Percentage) and st.from_type(TaxRate) work the same way, but on an individual type basis.

[click] Heads up though — Hypothesis's annotated-types support is still pretty basic. Nested Annotated aliases can fail to resolve entirely, and constraints like Timezone, IsNotNan, or IsFinite aren't well supported yet. Don't lean on it for everything.
-->
