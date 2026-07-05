---
layout: default
class: code-center
---


# <span class="slide-title-code">Pydantic</span> & <span class="slide-title-code">FastAPI</span>: composable schemas

<div class="divider-yellow"></div>

<p class="slide-tagline">Same types for validation and OpenAPI out of the box.</p>

````md magic-move {lines: true}
```python
class CreateReservationSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    room_id: RoomId
    guest_count: GuestCount
    starts_at: StayDate
    ends_at: StayDate
    rate: RoomRate
```

```python
class CreateReservationSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    room_id: Annotated[RoomId, Field(title="Room ID")]
    guest_count: GuestCount
    starts_at: StayDate
    ends_at: StayDate
    rate: RoomRate
```
````

<!--
Now for the API side. Same aliases, new reader — Pydantic validates the incoming data, and FastAPI turns it straight into OpenAPI docs.

RoomId, GuestCount, StayDate, and RoomRate are exactly the same aliases we declared before. Pydantic reads the annotated-types constraints, MinLen, Ge, Le, Gt, straight off the type and uses them to parse and validate incoming data.

[click] Need API-only stuff, like a title on room_id here? Wrap it in Annotated and stack a Field.
-->
