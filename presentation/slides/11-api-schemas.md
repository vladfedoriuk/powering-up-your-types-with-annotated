---
layout: default
class: code-center
---


# <span class="slide-title-code">Pydantic</span> & <span class="slide-title-code">FastAPI</span>: composable schemas

<div class="divider-yellow"></div>

<p class="slide-tagline">Same types for validation and OpenAPI out of the box.</p>

```python
class CreateReservationSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    room_id: RoomId
    guest_count: GuestCount
    starts_at: StayDate
    ends_at: StayDate
    rate: RoomRate
```

<!--
Same Annotated types, new reader. Pydantic validates incoming data and FastAPI generates OpenAPI docs — nothing new to declare.

RoomId, GuestCount, StayDate, RoomRate are the exact same aliases used in the SQLAlchemy models. Pydantic reads the annotated_types constraints (MinLen, Ge, Le, Gt) for validation. It silently ignores the mapped_column() metadata — each tool reads only what it understands.

When adding API-specific metadata (description, title, alias), wrap with Annotated and stack a Field — don't use field = Field(...) assignment syntax. The domain alias stays unchanged.
-->
