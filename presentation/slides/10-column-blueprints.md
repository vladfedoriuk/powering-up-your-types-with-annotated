---
layout: default
class: code-center
---


# <span class="slide-title-code">SQLAlchemy</span>: reusable column blueprints

<div class="divider-blue"></div>

<p class="slide-tagline">ORM config in the alias — table-specific constraints on the field.</p>

````md magic-move {lines: true}
```python
# Step 1: Domain type alias — type constraint only
RoomId = Annotated[str, MinLen(1), MaxLen(20)]
TimestampTz = Annotated[datetime.datetime, Timezone(...)]
```

```python
# Step 2: Add ORM config to the alias — type-level only
RoomId = Annotated[
    str,
    MinLen(1),
    MaxLen(20),
    mapped_column(sa.String(20)),
]
TimestampTz = Annotated[
    datetime.datetime,
    Timezone(...),
    mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.current_timestamp()
    ),
]
```

```python
# Step 3: Use the aliases in a model
Identity = Annotated[
    int,
    Gt(0),
    mapped_column(sa.Integer(), sa.Identity(always=False), primary_key=True),
]


@registry.mapped_as_dataclass
class Room:
    __tablename__ = "rooms"

    id: Mapped[Identity] = mapped_column(init=False)
    room_id: Mapped[RoomId] = mapped_column(unique=True, index=True)
    rate: Mapped[RoomRateColumn]
    created_at: Mapped[TimestampTz]
```
````

<!--
The alias carries what's always true about the type — SQL type, nullability, server defaults.
unique=True and index=True are table decisions, not type decisions. They go on the field.

SQLAlchemy merges both mapped_column() calls: alias provides the type config, field provides the table-specific options.

Mapping approach is a separate choice — any of these work with the same aliases:
- DeclarativeBase subclass (classic)
- @registry.mapped_as_dataclass (shown here — keeps the class a plain Python dataclass)
- MappedAsDataclass base class
- registry.map_imperatively() for fully separate domain/table definitions
-->
