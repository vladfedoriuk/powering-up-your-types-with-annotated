---
layout: default
---

# persistence layer: sqlalchemy

<div class="divider-blue"></div>

## composition over inheritance

- **Decoupled domain**: core models don't subclass DB-specific base classes
- **Orthogonal layering**: ORM-specific metadata is layered onto types
- **Declarative structure**: database constraints map to domain constraints

<!--
Now we look at the persistence layer using SQLAlchemy.

Rather than polluting our pure domain model by inheriting from a database-specific base model, we use composition. We overlay persistence metadata using typing.Annotated, allowing our models to be mapped to tables while keeping them clean.
-->

---
layout: default
---

# reusable column blueprints

<div class="divider-blue"></div>

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

---
layout: default
---

# mapping types: `type_annotation_map`

<div class="divider-blue"></div>

- **Global mappings**: mapping custom Python type hints to database types
- **Distinct representations**: map different custom types to different column types

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
SQLAlchemy's type_annotation_map lets us configure global column rules.

We map our semantic types directly to database column types in the Declarative base class. At model declaration time, typing Mapped[RoomId] is enough for SQLAlchemy to resolve it to a VARCHAR(20) column. This eliminates field-level column declarations completely.
-->

---
layout: default
---

# generic column blueprints

<div class="divider-blue"></div>

- **Generic type parameters**: define blueprints that work for any inner type
- **PEP 695 generic alias**: clean spelling using `type X[T] = ...`

```python
# PEP 695 generic PrimaryKey blueprint
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

---
layout: default
---

# generating migrations

<div class="divider-blue"></div>

- **Metadata extraction**: Alembic reads type definitions to auto-generate schemas
- **Independent schemas**: database definitions can evolve around the domain

```bash
# Generate database migrations via Alembic
alembic revision --autogenerate -m "Initial migrations"

# Apply migrations
alembic upgrade heads
```

<!--
Once our SQLAlchemy models are declared, Alembic scans the registry metadata and autogenerates migration scripts.

The DB columns are derived directly from the Annotated types, showing that our persistence schemas adapt to our domain models instead of dictating them.
-->
