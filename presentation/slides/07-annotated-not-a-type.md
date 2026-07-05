---
layout: default
class: code-center
---


# <span class="slide-title-code">Annotated</span> is not a type

<div class="divider-red"></div>

<p class="slide-tagline">Special form — not assignable to <code>type[T]</code>.</p>

```python
from typing import Annotated

type(Annotated[int, "x"])
# <class 'typing._AnnotatedAlias'>

isinstance(Annotated[int, "x"], type)
# False
```

<!--
Another key thing to understand: Annotated is not a type. It's a "special form" — closer to a syntax keyword than a concrete Python class.

At runtime, wrapping something in Annotated produces a private `_AnnotatedAlias` object. That means it fails `isinstance` checks against `type`.

Because of this, if a library expects a `type`, passing an `Annotated` type will cause type checkers to reject it.
-->
