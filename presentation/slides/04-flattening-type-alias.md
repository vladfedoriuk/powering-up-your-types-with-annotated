---
layout: default
class: code-center
---

# Aliases block flattening

<div class="divider-blue"></div>

<p class="slide-tagline">PEP 695 <code>type</code> aliases are <em>lazy</em> — outer <code>Annotated</code> cannot see inside until evaluated.</p>

```python
from typing import Annotated
from annotated_types import MinLen, MaxLen

type Inner = Annotated[int, MinLen(1)]

Annotated[Inner, MaxLen(100)].__metadata__
# (MaxLen(100),)  ← MinLen(1) is hidden inside Inner

Annotated[Inner, MaxLen(100)] == Annotated[int, MinLen(1), MaxLen(100)]
# False  ← alias breaks equality too
```

<!--
When you put Annotated behind a type alias, flattening stops working.

This is because these type aliases are evaluated lazily. The outer Annotated sees only one opaque object, hiding the inner metadata and breaking direct type comparison.

Because of this, library authors have to explicitly evaluate aliases to find those hidden constraints.
-->
