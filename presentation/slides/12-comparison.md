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
