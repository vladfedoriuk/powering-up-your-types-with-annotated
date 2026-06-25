---
layout: default
class: code-center
---


# introspecting annotated

<div class="divider-red"></div>

<p class="slide-tagline"><code>get_constraints()</code> — pattern Pydantic uses.</p>

```python
from typing import Annotated, get_args, get_origin
from annotated_types import BaseMetadata, GroupedMetadata

def get_constraints(tp):
    assert get_origin(tp) is Annotated
    for arg in get_args(tp)[1:]:        # [0] is the base type
        if isinstance(arg, BaseMetadata):
            yield arg
        elif isinstance(arg, GroupedMetadata):
            yield from arg              # e.g. Interval → Gt + Lt
```

<!--
Here's the canonical pattern that Pydantic and other Annotated-aware libraries use to extract constraints from type annotations.

The function takes an Annotated type and yields all the BaseMetadata and GroupedMetadata objects from its metadata tuple.

The key insight is in how get_args works. The first element, at index zero, is the base type — str, int, Decimal, whatever your values actually are. Everything from index one onwards is metadata.

For simple constraints like Gt or MinLen, they're instances of BaseMetadata, so you yield them directly.

For grouped constraints like Interval or Len, they implement the GroupedMetadata protocol, which means they're iterable. Interval yields Gt and Lt. Len yields MinLen and MaxLen. So you yield from them to unpack the individual constraints.

This is the contract that annotated-types establishes for the whole ecosystem. If you're a constraint, you're either BaseMetadata or GroupedMetadata. Libraries do isinstance checks against these two contracts, and the whole system stays loosely coupled.
-->
