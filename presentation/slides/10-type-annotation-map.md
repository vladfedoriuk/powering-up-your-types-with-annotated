---
layout: default
class: code-center
---


# Mapping types: <span class="slide-title-code">type_annotation_map</span>

<div class="divider-blue"></div>

<p class="slide-tagline">Global Python type → SQL column mapping.</p>

```python
class Base(DeclarativeBase):
    type_annotation_map = {
        RoomId: sqlalchemy.String(20),
        RoomRate: sqlalchemy.Numeric(precision=10, scale=2),
        StayDate: sqlalchemy.Date(),
    }
@registry.mapped_as_dataclass
class Reservation:
    id: Mapped[Identity] = mapped_column(init=False)
    room_id: Mapped[RoomId]
    rate: Mapped[RoomRate]
```

<!--
Register Annotated types → SQL column types once in the base class. Writing Mapped[RoomId] is enough — SQLAlchemy resolves VARCHAR(20) automatically. No per-field declarations.
-->
