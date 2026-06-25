---
layout: default
class: code-center
---


# composable api schemas

<div class="divider-yellow"></div>

<p class="slide-tagline">Reuse domain aliases in Pydantic schemas.</p>

```python
class ReservationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    reference: Annotated[
        OrderReference,
        Field(serialization_alias="ref", title="The reservation reference"),
    ]
    guest_count: GuestCount
    rate: RoomRate
    created_at: TimestampTz
```

<!--
Pydantic schemas leverage the exact same semantic type aliases defined in our domain.

By using RoomId, GuestCount, and RoomRate inside our BaseModel, we inherit validation and serialization rules. If we need to customize API-specific parameters (like a JSON serialization alias), we just stack a Pydantic Field on top.
-->
