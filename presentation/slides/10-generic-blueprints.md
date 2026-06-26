---
layout: default
class: code-center
---


# Generic column blueprints

<div class="divider-blue"></div>

<p class="slide-tagline">PEP 695 generic column blueprints.</p>

```python
type PrimaryKey[T] = Annotated[
    T,
    mapped_column(sa.Integer(), sa.Identity(always=False), primary_key=True),
]


@registry.mapped_as_dataclass
class Room:
    id: Mapped[PrimaryKey[int]] = mapped_column(init=False)
    room_id: Mapped[RoomId]
```

<!--
PrimaryKey[T] — write the column options once, reuse across any type. PrimaryKey[int], PrimaryKey[uuid.UUID] — same blueprint, different base type. Requires SQLAlchemy 2.0.44+.
-->
