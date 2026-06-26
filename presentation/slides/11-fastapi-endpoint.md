---
layout: default
class: code-center
---


# Fits together with <span class="slide-title-code">FastAPI</span>

<div class="divider-yellow"></div>

```python
@app.get("/rooms/{room_id}")
async def get_room(
    room_id: Annotated[RoomId, Path(title="Room ID")],
    services: svcs.fastapi.DepContainer,
) -> RoomResponse: ...


@app.post("/reservations/", status_code=status.HTTP_201_CREATED)
async def create_reservation(
    data: CreateReservationSchema,
    services: svcs.fastapi.DepContainer,
) -> ReservationSchema:
    repo = await services.aget(RoomRepository)
    room = await repo.get_by_room_id(data.room_id)
    room.add_reservation(
        reservation := Reservation(
            room_id=data.room_id, guest_count=data.guest_count, rate=data.rate
        )
    )
    # ...
```

<!--
RoomId defined once — used in SQLAlchemy models, Pydantic schemas, and FastAPI path parameters. Each layer reads only what it understands.

You can keep layering. Annotated[RoomId, Path(title="Room ID")] adds a framework-level label on top of the domain type without touching the alias. Same pattern — new reader, new metadata, same type underneath.
-->
