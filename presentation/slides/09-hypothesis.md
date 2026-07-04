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
The factory test was example-based — one scenario, one assertion. Property-based testing flips that: describe properties that should always hold, and Hypothesis generates hundreds of random inputs to verify them.

[click] `st.builds` reads the dataclass and generates every field from their Annotated constraints — guest_count, room_id, starts_at, ends_at, all automatic.

[click] `st.from_type` does the same for individual types. Percentage and TaxRate both have Annotated constraints, so Hypothesis knows what valid values look like.

[click] One caveat — Hypothesis's Annotated support is still basic. Nested aliases can fail to resolve, and constraints like Timezone or IsFinite aren't well supported yet. You might still write a strategy by hand sometimes.
-->
