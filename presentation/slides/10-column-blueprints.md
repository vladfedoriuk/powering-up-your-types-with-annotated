---
layout: default
class: code-center
---


# Reusable column blueprints

<div class="divider-blue"></div>

<p class="slide-tagline"><code>mapped_column</code> inside the type alias.</p>

````md magic-move {lines: true}
```python
# Step 1: Pure Domain Type
RoomId = Annotated[str, MinLen(1), MaxLen(20)]
TimestampTz = Annotated[datetime.datetime, Timezone(...)]
```

```python
# Step 2: Overlay SQLAlchemy mapped_column details
RoomId = Annotated[
    str,
    MinLen(1),
    MaxLen(20),
    mapped_column(sqlalchemy.String(20), nullable=False, index=True, unique=True),
]

TimestampTz = Annotated[
    datetime.datetime,
    Timezone(...),
    mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.current_timestamp(),
    ),
]
```
````

<!--
We can layer database columns directly inside our semantic type definitions.

By wrapping mapped_column inside our Annotated type aliases, we create reusable blueprints. Whenever we write a model and type a field as RoomId or TimestampTz, SQLAlchemy automatically extracts the column properties (like indexes, unique constraints, nullability, and database defaults) without repeating them.
-->
