---
layout: default
class: code-center
---


# Nesting flattens

<div class="divider-blue"></div>

<p class="slide-tagline">Nested <code>Annotated</code> merges into one tuple — inner metadata first.</p>

```python
from typing import Annotated
from annotated_types import MinLen, MaxLen

Inner = Annotated[int, MinLen(1)]
Outer = Annotated[Inner, MaxLen(100)]  # nested Annotated flattens

Outer.__metadata__  # (MinLen(1), MaxLen(100))  ← inner metadata first
Outer == Annotated[int, MinLen(1), MaxLen(100)]  # True
```

<!--
When you nest Annotated directly, Python automatically flattens it.

The metadata from the inner type comes first, followed by the outer one. This means they combine into a single tuple, and type comparison works exactly as you'd expect.

But this only happens when you nest them directly. Next, we'll see where this breaks.
-->
