---
layout: default
class: code-center
---

# Fits together with <span class="slide-title-code">FastAPI</span>

<div class="divider-yellow"></div>

```python {all|3|4|all}
@app.get("/rooms/{room_id}")
async def get_room(
    room_id: Annotated[RoomId, Path(title="Room ID")],
    services: svcs.fastapi.DepContainer,  # Annotated[Container, Depends(container)]
) -> RoomResponse: ...


@app.post("/reservations/", status_code=status.HTTP_201_CREATED)
async def create_reservation(
    data: CreateReservationSchema,
    services: svcs.fastapi.DepContainer,
) -> ReservationSchema:
    service = await services.aget(ReservationService)
    reservation = await service.place(data)
    return ReservationSchema.model_validate(reservation, from_attributes=True)
```

<!--
RoomId shows up here too, now as a FastAPI path parameter.

[click] The annotated room ID with a path title is basically what we just did with Field, just for path parameters this time.

[click] DepContainer is Annotated too — it's the dependency injection from earlier.

[click] So, where does it bring us from here?
-->
