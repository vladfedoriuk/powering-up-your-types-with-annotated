---
layout: default
class: code-center
---


# PEP 563 caveat

<div class="divider-yellow"></div>

<p class="slide-tagline"><code>from __future__ import annotations</code> stores strings.</p>

```python
from __future__ import annotations
from typing import Annotated, get_type_hints
from annotated_types import MinLen, MaxLen, Gt

Name = Annotated[str, MinLen(1), MaxLen(100)]

class Product:
    name: Name
    price: Annotated[Decimal, Gt(0)]

Product.__annotations__
# {'name': 'Name', 'price': 'Annotated[Decimal, Gt(0)]'}  ← strings!

get_type_hints(Product, include_extras=True)
# {'name': Annotated[str, MinLen(1), MaxLen(100)], ...}    ← resolved
```

<!--
There's an important caveat when working with PEP 563 — the from __future__ import annotations statement that many projects use.

When this future import is active, Python stores all annotations as raw strings. It never evaluates them. So Product.__annotations__ gives you the dictionary with string values: 'Name' and 'Annotated[Decimal, Gt(0)]'.

If you call annotationlib.get_annotations with Format.VALUE, you get these strings as-is — it does not evaluate them. You need to pass eval_str=True to make it resolve the strings against the module globals.

Alternatively, typing.get_type_hints always evaluates strings — it was designed for this. With include_extras=True, you get the fully resolved Annotated types with all their metadata intact.

One more thing: under PEP 563, Python 3.14 sets __annotate__ to None rather than a callable function. This is because the compiler never generates the PEP 649 lazy evaluator when annotations are stored as strings. So if you're checking for __annotate__, be aware it exists but is None.

The good news is that PEP 649, which is the default in Python 3.14, fixes all of this with true lazy evaluation.
-->
