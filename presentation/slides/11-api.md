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
