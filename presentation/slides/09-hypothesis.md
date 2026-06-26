---
layout: default
class: code-center
---


# Hypothesis: property-based testing

<div class="divider-red"></div>

<p class="slide-tagline"><code>st.builds</code> for objects, <code>st.from_type</code> reads <code>Annotated</code> constraints directly.</p>

```python
@given(
    starts_at=st.dates(),
    nights=st.integers(min_value=1, max_value=30),
    guest_count=st.from_type(GuestCount),
    discount=st.from_type(Percentage),
    tax=st.from_type(TaxRate),
)
def test_stay_total_never_negative(starts_at, nights, guest_count, discount, tax):
    reservation = Reservation(
        room_id="101",
        guest_count=guest_count,
        starts_at=starts_at,
        ends_at=starts_at + timedelta(days=nights),
        rate=Decimal("100"),
    )
    assert calculate_stay_total(reservation, discount, tax) >= 0
```

<!--
st.from_type(GuestCount) generates integers between 1 and 10 — straight from the Annotated constraints. Same for Percentage and TaxRate.

Limitation: nested or flattened Annotated aliases like RoomRate (which has Predicate metadata) may fail with ResolutionFailed in some Hypothesis versions. Timezone, IsNotNan, IsFinite are also not supported. Use explicit strategies (st.decimals, st.dates) for those cases — as shown here with rate fixed to a safe value.
-->
