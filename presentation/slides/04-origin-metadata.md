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
Every Annotated type has two main attributes: `__origin__` and `__metadata__`.

`__origin__` gives you the base type — `str` in this case. `__metadata__` is a tuple that keeps all constraints in the order you defined them.

One quick catch: helper function `get_origin` returns `Annotated` itself, not the base type. To get the base type, read `__origin__` directly.
-->
