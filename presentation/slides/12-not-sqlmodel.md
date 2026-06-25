---
layout: default
class: code-center
---


# "no, it is not like sqlmodel"

<div class="divider-red"></div>

<p class="slide-tagline">One class for ORM + API — breaks when contracts diverge.</p>

```python
class RoomBase(SQLModel):
    room_id: RoomId = Field(index=True, unique=True, max_length=20)
    capacity: GuestCount = Field(ge=1, le=10)

class Room(RoomBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
```

<!--
SQLModel attempts to merge Pydantic and SQLAlchemy. While this works beautifully for simple CRUD applications, it forces a tight coupling between database tables and API schemas.

As soon as your write schema needs to hide internal fields or map columns differently than the read schema, you are forced to inherit and split classes, fracturing the "single model" promise and deferring design pressure.
-->
