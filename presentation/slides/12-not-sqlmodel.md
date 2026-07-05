---
layout: default
class: code-center
---


# The SQLModel way

<div class="divider-red"></div>

```python
class RoomBase(SQLModel):
    room_id: RoomId = Field(index=True, unique=True, max_length=20)
    capacity: GuestCount = Field(ge=1, le=10)


class Room(RoomBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
```

<!--
SQLModel merges Pydantic and SQLAlchemy into one class — great for simple CRUD, but it ties your database table to your API schema.

The moment your write schema needs to hide a field or shape data differently than the read schema, you're splitting classes again.
-->
