---
layout: default
class: code-center
---


# Validation & serialization as metadata

<div class="divider-yellow"></div>

<div class="flex flex-wrap gap-x-3 gap-y-3 mt-4 mb-4 font-mono text-sm">
  <span class="pill pill--red">BeforeValidator</span>
  <span class="pill pill--yellow">AfterValidator</span>
  <span class="pill pill--blue">PlainValidator</span>
  <span class="pill pill--red">WrapValidator</span>
  <span class="pill pill--yellow">WithJsonSchema</span>
  <span class="pill pill--blue">PlainSerializer</span>
</div>

````md magic-move {lines: true}
```python
# Step 1: Base constraint type
Amount = Annotated[Decimal, Gt(0)]
```

```python
# Step 2: Overlay validation, serialization & usage
Amount = Annotated[
    Decimal,
    Gt(0),
    WrapValidator(lambda v, handler: handler(v).quantize(Decimal("0.01"))),
    PlainSerializer(lambda v: float(v), return_type=float, when_used="always"),
]

ta = TypeAdapter(Amount)
assert ta.validate_python(Decimal("10.123")) == Decimal("10.12")
assert ta.validate_python(10.456) == Decimal("10.46")
assert ta.dump_json(Decimal("10.12")) == b"10.12"
```
````

<!--
Pydantic ships its own functional validators and serializers, and they just slot into Annotated right alongside Gt or MinLen.

[click] WrapValidator rounds the Decimal to two places after Pydantic validates it, and PlainSerializer turns it into a float for both Python and JSON output.
-->
