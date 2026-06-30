---
layout: default
class: code-center
---


# <span class="slide-title-code">\_\_origin\_\_</span> and <span class="slide-title-code">\_\_metadata\_\_</span>

<div class="divider-blue"></div>

<p class="slide-tagline"><code>__origin__</code> is the base type; <code>get_origin()</code> returns <code>Annotated</code>.</p>

```python
from typing import Annotated, get_origin
from annotated_types import MinLen, MaxLen

Name = Annotated[str, MinLen(1), MaxLen(100)]

Name.__origin__  # str
Name.__metadata__  # (MinLen(1), MaxLen(100))

get_origin(Name)  # Annotated  ← not str!
```

<!--
Every Annotated type has two runtime attributes library authors rely on.

__origin__ is the unwrapped base type — str here. __metadata__ is a tuple of every metadata argument, in order.

Common gotcha: get_origin(Name) returns Annotated itself, not str. For the base type, use __origin__ or get_args(Name)[0].

Order matters — Annotated[int, A, B] != Annotated[int, B, A]. Duplicates are preserved; metadata is never deduplicated.
-->
