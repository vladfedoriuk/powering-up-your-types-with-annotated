---
layout: default
class: code-center
---


# Validators as metadata

<div class="divider-yellow"></div>

<p class="slide-tagline"><code>BeforeValidator</code> & <code>PlainSerializer</code> as metadata.</p>

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
