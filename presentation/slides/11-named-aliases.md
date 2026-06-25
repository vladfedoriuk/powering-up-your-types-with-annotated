---
layout: default
class: code-center
---


# Implicit vs named type aliases

<div class="divider-yellow"></div>

<p class="slide-tagline">PEP 695 named aliases → JSON Schema <code>$ref</code>.</p>

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
