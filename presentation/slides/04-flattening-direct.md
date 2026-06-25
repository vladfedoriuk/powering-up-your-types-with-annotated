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

Annotated[
    Annotated[int, MinLen(1)],
    MaxLen(100),
] == Annotated[int, MinLen(1), MaxLen(100)]  # True
```

<!--
When you nest Annotated directly, Python flattens automatically. Inner constraints come first, outer constraints after. Same type object, same __metadata__ tuple.

This is the happy path — most hand-written nesting behaves as you'd expect.
-->
