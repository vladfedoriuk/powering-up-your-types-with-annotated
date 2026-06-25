---
layout: default
---

# building the domain

<div class="divider-red"></div>

## reservations, resources, and rules

- Start with a clean, framework-independent domain model
- Domain rules are defined and enforced at class boundaries
- Semantic types replace raw primitives to make constraints explicit

<!--
We will now build a realistic room reservation domain to demonstrate how typing.Annotated enables cleaner architecture through composition.

Our domain is centered on Rooms and Reservations, with core business logic like calculating stays and guarding capacity constraints. We start with a pure domain model, completely free of databases or API frameworks.
-->

---
layout: default
---

# pure domain model

<div class="divider-red"></div>

```python
@dataclass
class Reservation:
    room_id: str
    guest_count: int
    starts_at: datetime.date
    ends_at: datetime.date
    rate: Decimal

@dataclass
class Room:
    room_id: str
    capacity: int
    reservations: list[Reservation] = field(default_factory=list)

    def add_reservation(self, reservation: Reservation) -> None:
        if reservation.guest_count > self.capacity:
            raise ValueError("Exceeds room capacity")
        ...
```

<!--
Here is our initial pure domain model. Note that fields like room_id and capacity are typed as raw strings and integers.

The Room class aggregates its Reservations and enforces rules like capacity validation directly inside its add_reservation method. There is no infrastructure logic here.
-->

---
layout: default
---

# from primitive to semantic

<div class="divider-red"></div>

````md magic-move {lines: true}
```python
# Step 1: Primitive types
@dataclass
class Reservation:
    room_id: str
    guest_count: int
    rate: Decimal
    created_at: datetime.datetime
```

```python
# Step 2: Swap to rich semantic types
RoomId = Annotated[str, MinLen(1), MaxLen(20)]
GuestCount = Annotated[int, Ge(1), Le(10)]
RoomRate = Annotated[Amount, Gt(0)]
TimestampTz = Annotated[datetime.datetime, Timezone(...)]

@dataclass
class Reservation:
    room_id: RoomId
    guest_count: GuestCount
    rate: RoomRate
    created_at: TimestampTz
```
````

<!--
Using shiki-magic-move, we can transition from primitive types to semantic type aliases parameterized with annotated-types constraints.

By swapping out raw primitives for rich aliases like RoomId, GuestCount, and RoomRate, the domain constraints become self-documenting and are declared directly in the type system.
-->

---
layout: default
---

# polyfactory: test data

<div class="divider-red"></div>

- **Respects constraints**: generated properties automatically conform to constraints
- **Zero config**: type factories resolve annotations out-of-the-box

```python
from polyfactory.factories.dataclasses import DataclassFactory

class ReservationFactory(DataclassFactory[Reservation]):
    __model__ = Reservation

# Generates valid Reservation with room_id length <= 20 and rate > 0
mock_res = ReservationFactory.build()
```

<!--
For automated testing, polyfactory reads the Annotated constraints.

Since the constraints are part of the type signature, the ReservationFactory can automatically generate mock reservations that comply with the GuestCount limit and RoomRate constraints without requiring any manual configuration.
-->

---
layout: default
---

# hypothesis: property-based testing

<div class="divider-red"></div>

- **Edge-case discovery**: generates diverse, unexpected inputs to find bugs
- **Constraint inference**: derives testing strategies directly from types

```python
@given(
    reservation=st.builds(Reservation),
    discount=st.from_type(Percentage),
    tax=st.from_type(TaxRate),
)
def test_stay_total_non_negative(reservation, discount, tax):
    total = calculate_stay_total(reservation, discount, tax)
    assert total >= 0
```

<!--
For bulletproof testing, we use Hypothesis.

By running st.from_type, Hypothesis automatically generates arbitrary valid inputs matching the Gt, Le, and Ge constraints of our type aliases. This makes it easy to assert properties like stay totals always remaining non-negative. Note that for complex nested annotations, custom strategies are sometimes still needed.
-->

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

---
layout: default
---

# api layer: pydantic & fastapi

<div class="divider-yellow"></div>

## the interface layer

- **Independent contracts**: API schemas map to domain types without tight coupling
- **Type-driven endpoints**: validation and serialization are inferred from types
- **Automatic docs**: OpenAPI schemas are generated directly from annotations

<!--
Now let's look at the API layer with FastAPI and Pydantic.

Just like the persistence layer, the API layer hooks into our domain models and semantic types. Pydantic reads the annotations to validate incoming HTTP requests and serialize outgoing JSON payloads automatically.
-->

---
layout: default
---

# composable api schemas

<div class="divider-yellow"></div>

- **Dry structures**: reuse semantic types instead of re-declaring constraints
- **Field customizations**: layer API-specific metadata on top of domain types

```python
class ReservationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    reference: Annotated[
        OrderReference,
        Field(serialization_alias="ref", title="The reservation reference"),
    ]
    guest_count: GuestCount
    rate: RoomRate
    created_at: TimestampTz
```

<!--
Pydantic schemas leverage the exact same semantic type aliases defined in our domain.

By using RoomId, GuestCount, and RoomRate inside our BaseModel, we inherit validation and serialization rules. If we need to customize API-specific parameters (like a JSON serialization alias), we just stack a Pydantic Field on top.
-->

---
layout: default
---

# validators as metadata

<div class="divider-yellow"></div>

````md magic-move {lines: true}
```python
# Step 1: Base constraint type
Amount = Annotated[Decimal, IsFinite, IsNotNan]
```

```python
# Step 2: Overlay validation & serialization rules
def trim_str(v: str) -> str:
    return v.strip()

def serialize_amount(v: Decimal) -> float:
    return float(v.quantize(Decimal("0.01")))

RoomId = Annotated[str, BeforeValidator(trim_str), MinLen(1), MaxLen(20)]

Amount = Annotated[
    Decimal,
    IsFinite,
    IsNotNan,
    PlainSerializer(serialize_amount, return_type=float, when_used="json"),
]
```
````

<!--
Pydantic provides specialized metadata objects like BeforeValidator and PlainSerializer.

We can place these directly inside our Annotated aliases. For example, RoomId automatically strips leading/trailing whitespaces before validation, and Amount automatically serializes Decimal values to float strings during JSON serialization. All this happens transparently.
-->

---
layout: default
---

# implicit vs named type aliases

<div class="divider-yellow"></div>

- **Implicit**: resolved inline, duplicates schema definitions
- **Named (PEP 695)**: preserved as `$ref` in JSON Schema (Pydantic v2.11+)

```python
# Implicit: inlined everywhere (duplicated schema)
PositiveInt = Annotated[int, Gt(0)]

# Named: produces a single $defs entry referenced via $ref
type PositiveInt = Annotated[int, Gt(0)]
```

<!--
An important distinction in Pydantic is how it handles type aliases in JSON Schema generation.

Implicit assignment aliases are resolved inline, which duplicates schemas. PEP 695 named type aliases are compiled as a single schema entry inside $defs and referenced via $ref. This is critical for keeping large schemas clean and supporting recursive types.
-->

---
layout: default
---

# standalone validation

<div class="divider-yellow"></div>

- **Standalone checks**: validate raw Python values outside models
- **TypeAdapter API**: parse, validate, and serialize any type directly

```python
from pydantic import TypeAdapter

# Create adapter for a semantic type
rate_adapter = TypeAdapter(RoomRate)

# Validate raw values
rate_adapter.validate_python(Decimal("150.00"))  # ✓ Valid
rate_adapter.validate_python(Decimal("-10.00"))  # ✗ ValidationError
```

<!--
Sometimes you want to validate a value without defining a whole BaseModel.

Pydantic's TypeAdapter API allows you to wrap any Annotated type alias directly. You can use it to validate, serialize, or generate JSON schema for standalone values (like checking a query parameter or parsing a configuration variable).
-->

---
layout: default
---

# philosophical takeaway

<div class="divider-red"></div>

## how does it compare to standard patterns?

- **Django / Django Rest Framework**: Active Record & Table-Driven Design
- **SQLModel**: Shared inheritance models
- **Composition-Based Design**: Metadata-layered domain types

<!--
Let's zoom out and look at the architectural philosophy.

We will contrast our composition-based design using typing.Annotated with two very popular patterns in Python: Django/DRF and SQLModel.
-->

---
layout: default
---

# "no, it is not like django"

<div class="divider-red"></div>

- **Table-centric coupling**: the DB model defines the domain and API
- **Design pressure**: database column changes ripple through the entire app

```python
# Django: DB table shape forces the API serializer contract
class Room(models.Model):
    room_id = models.CharField(max_length=20, unique=True, db_index=True)
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_id", "capacity"]
```

<!--
Django uses the Active Record pattern. The database table shape is the single model that dictates everything.

When a DB field evolves, that change ripples through your serializer, validation checks, and views. There is no independent domain layer. The database exerts continuous design pressure on your entire code structure.
-->

---
layout: default
---

# "no, it is not like sqlmodel"

<div class="divider-red"></div>

- **Shared inheritance**: one class for both ORM and API schema
- **Friction points**: breaks down when read and write API contracts diverge

```python
# SQLModel: unifies ORM and Pydantic, but couples table to API
class RoomBase(SQLModel):
    room_id: RoomId = Field(index=True, unique=True, max_length=20)
    capacity: GuestCount = Field(ge=1, le=10)

class Room(RoomBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
```

<!--
SQLModel attempts to merge Pydantic and SQLAlchemy. While this works beautifully for simple CRUD applications, it forces a tight coupling between database tables and API schemas.

As soon as your write schema needs to hide internal fields or map columns differently than the read schema, you are forced to inherit and split classes, fracturing the "single model" promise and deferring design pressure.
-->

---
layout: default
---

# composition-based design

<div class="divider-red"></div>

- **Decoupled concerns**: domain is central; persistence & API are extensions
- **Lens model**: metadata acts as stackable, transparent lenses on a base type

> "The type is the contract. The metadata is the instruction manual — and each reader only reads the pages written for them."

<!--
With typing.Annotated, the type is the contract, and metadata is the instruction manual.

The domain type is defined independently in the center. SQLAlchemy reads the persistence metadata, Pydantic reads validation rules, and other tools read only what they understand. Each layer is completely decoupled, removing design pressure and keeping your architecture clean and maintainable.
-->

---
layout: default
---

# pandera: dataframe validation

<div class="divider-blue"></div>

## tabular data metadata

- **Tabular type safety**: validate DataFrame columns and types at runtime
- **Single source of truth**: embed column ranges, unique checks, and descriptions

```python
import pandera as pa
from pandera.typing import Series

class ReservationModel(pa.DataFrameModel):
    room_id: Annotated[Series[str], pa.Field(unique=True)]
    guest_count: Annotated[Series[int], pa.Field(ge=1, le=10)]
    rate: Annotated[Series[float], pa.Field(gt=0)]

# Validates column types, unique constraints, and min/max ranges
ReservationModel.validate(dataframe)
```

<!--
Pandera is a fantastic example of the Python ecosystem embracing typing.Annotated for dataframe validation.

By using Series[T] wrapped in Annotated with pa.Field metadata, you define high-level constraints like column uniqueness, numeric ranges, and metadata descriptions. The dataframe is verified at runtime against this single source of truth.
-->

---
layout: default
---

# documentation: `annotated-doc`

<div class="divider-yellow"></div>

- **Self-documenting code**: inline descriptions stored directly in type signatures
- **Tooling integration**: supported by `mkdocstrings` and documentation tools

```python
from annotated_doc import Doc

FIRST_ORDER_DISCOUNT: Annotated[
    Percentage,
    Doc("Discount percentage applied to the first reservation made by a guest"),
] = Decimal(15)
```

<!--
For our final layer, we look at documentation.

annotated-doc introduces the Doc metadata object, which was proposed in the revoked PEP 727. It allows you to document constants, parameters, or fields directly inside their types. Sebastian Ramirez championed this pattern, and it powers Typer and FastAPI's internal documentation rendering.
-->

---
layout: default
class: text-center
---

# thank you!

<div class="flex flex-col items-center justify-center mt-10">
  <QRCode value="https://github.com/vladfedoriuk/powering-up-your-types-with-annotated" :size="200" render-as="svg" />
</div>

<br />

## questions?

<!--
Thank you for attending this talk on typing.Annotated!

We have covered how Annotated breaks the static/runtime barrier, acts as a composable metadata engine, and decouples our domain from SQL databases, API schemas, and documentation tools.

I am open to any questions you may have.
-->
