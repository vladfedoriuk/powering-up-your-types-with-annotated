---
layout: default
class: code-center
---

# Make your types mean something

<div class="divider-red"></div>

<p class="slide-tagline">Name what data is — and what's valid.</p>

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
We swap the raw primitives for Annotated aliases.

[click] `RoomId` is still a string under the hood, and `GuestCount` is still an integer. But now, constraints like minimum length and value ranges live directly inside the type declarations.

This keeps the constraints right next to the specific domain types they describe.

When we say something is a `RoomRate`, we're not just saying it's a decimal — we're saying exactly what kind of decimal it is.
-->
