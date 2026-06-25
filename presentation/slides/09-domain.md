---
layout: default
---

# building the domain

<div class="divider-red"></div>

## reservations, resources, and rules

- Start with a clean, framework-independent domain model
- Domain rules are defined and enforced at class boundaries
- Semantic types replace raw primitives to make constraints explicit

<!--
We will now build a realistic room reservation domain to demonstrate how typing.Annotated enables cleaner architecture through composition.

Our domain is centered on Rooms and Reservations, with core business logic like calculating stays and guarding capacity constraints. We start with a pure domain model, completely free of databases or API frameworks.
-->

---
layout: default
---

# pure domain model

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
Here is our initial pure domain model. Note that fields like room_id and capacity are typed as raw strings and integers.

The Room class aggregates its Reservations and enforces rules like capacity validation directly inside its add_reservation method. There is no infrastructure logic here.
-->

---
layout: default
---

# from primitive to semantic

<div class="divider-red"></div>

````md magic-move {lines: true}
```python
# Step 1: Primitive types
@dataclass
class Reservation:
    room_id: str
    guest_count: int
    rate: Decimal
    created_at: datetime.datetime
```

```python
# Step 2: Swap to rich semantic types
RoomId = Annotated[str, MinLen(1), MaxLen(20)]
GuestCount = Annotated[int, Ge(1), Le(10)]
RoomRate = Annotated[Amount, Gt(0)]
TimestampTz = Annotated[datetime.datetime, Timezone(...)]

@dataclass
class Reservation:
    room_id: RoomId
    guest_count: GuestCount
    rate: RoomRate
    created_at: TimestampTz
```
````

<!--
Using shiki-magic-move, we can transition from primitive types to semantic type aliases parameterized with annotated-types constraints.

By swapping out raw primitives for rich aliases like RoomId, GuestCount, and RoomRate, the domain constraints become self-documenting and are declared directly in the type system.
-->

---
layout: default
---

# polyfactory: test data

<div class="divider-red"></div>

- **Respects constraints**: generated properties automatically conform to constraints
- **Zero config**: type factories resolve annotations out-of-the-box

```python
from polyfactory.factories.dataclasses import DataclassFactory

class ReservationFactory(DataclassFactory[Reservation]):
    __model__ = Reservation

# Generates valid Reservation with room_id length <= 20 and rate > 0
mock_res = ReservationFactory.build()
```

<!--
For automated testing, polyfactory reads the Annotated constraints.

Since the constraints are part of the type signature, the ReservationFactory can automatically generate mock reservations that comply with the GuestCount limit and RoomRate constraints without requiring any manual configuration.
-->

---
layout: default
---

# hypothesis: property-based testing

<div class="divider-red"></div>

- **Edge-case discovery**: generates diverse, unexpected inputs to find bugs
- **Constraint inference**: derives testing strategies directly from types

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
