---
layout: default
class: code-center
---


# standalone validation

<div class="divider-yellow"></div>

<p class="slide-tagline">Validate any type without a <code>BaseModel</code>.</p>

```python
from pydantic import TypeAdapter

rate_adapter = TypeAdapter(RoomRate)

rate_adapter.validate_python(Decimal("150.00"))  # ✓ Valid
rate_adapter.validate_python(Decimal("-10.00"))  # ✗ ValidationError
```

<!--
Sometimes you want to validate a value without defining a whole BaseModel.

Pydantic's TypeAdapter API allows you to wrap any Annotated type alias directly. You can use it to validate, serialize, or generate JSON schema for standalone values (like checking a query parameter or parsing a configuration variable).
-->
