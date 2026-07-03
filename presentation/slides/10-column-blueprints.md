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
Testing's done, let's move on to persistence. Here are the same aliases we defined earlier — still just the type and its constraint, nothing SQL yet.

[click] Now the ORM config moves into the alias — SQL type, server defaults — because those are always true for the type.

[click] Here's the model using those aliases. Nullability, uniqueness, and indexes are all table decisions, so they land on the field, and SQLAlchemy merges both mapped_column() calls together — alias for the type, field for the table. And mapped_as_dataclass is just one way to wire this up — a classic DeclarativeBase subclass or the MappedAsDataclass base class work just as well with the same aliases.
-->
