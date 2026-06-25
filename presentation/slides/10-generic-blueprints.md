---
layout: default
class: code-center
---


# generic column blueprints

<div class="divider-blue"></div>

<p class="slide-tagline">PEP 695 generic column blueprints.</p>

```python
type PrimaryKey[T] = Annotated[
    T,
    mapped_column(primary_key=True, autoincrement=True),
]

@registry.mapped_as_dataclass
class Room:
    id: Mapped[PrimaryKey[int]] = mapped_column(init=False)
    room_id: Mapped[RoomId]
```

<!--
With PEP 695, we can write generic column blueprints using type aliases.

The PrimaryKey[T] alias wraps a mapped_column primary key definition. We can use it as PrimaryKey[int] or PrimaryKey[uuid.UUID]. SQLAlchemy 2.0.44+ resolves these generic aliases cleanly, ensuring that we write primary key declarations once and reuse them across all models.
-->
