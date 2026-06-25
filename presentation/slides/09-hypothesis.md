---
layout: default
class: code-center
---


# Hypothesis: property-based testing

<div class="divider-red"></div>

<p class="slide-tagline">Strategies inferred from <code>Annotated</code> aliases.</p>

```python
@given(
    reservation=st.builds(Reservation),
    discount=st.from_type(Percentage),
    tax=st.from_type(TaxRate),
)
def test_stay_total_non_negative(reservation, discount, tax):
    total = calculate_stay_total(reservation, discount, tax)
    assert total >= 0
```

<!--
For bulletproof testing, we use Hypothesis.

By running st.from_type, Hypothesis automatically generates arbitrary valid inputs matching the Gt, Le, and Ge constraints of our type aliases. This makes it easy to assert properties like stay totals always remaining non-negative. Note that for complex nested annotations, custom strategies are sometimes still needed.
-->
