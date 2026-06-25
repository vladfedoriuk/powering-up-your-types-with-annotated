---
layout: default
class: code-center
---


# From primitive to semantic

<div class="divider-red"></div>

<p class="slide-tagline">Swap primitives for constraint-rich aliases.</p>

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
