---
layout: default
class: code-center
---


# PEP 563 stores strings

<div class="divider-yellow"></div>

<p class="slide-tagline"><code>get_annotations(format.value)</code> returns strings — use <code>eval_str=True</code> or <code>get_type_hints</code>.</p>

```python
from __future__ import annotations
import annotationlib
from annotationlib import Format
from typing import get_type_hints


class Product:
    name: Name
    price: Price


Product.__annotations__
# {'name': 'Name', 'price': 'Price'}  ← strings

annotationlib.get_annotations(Product, format=Format.VALUE, eval_str=True)
get_type_hints(Product, include_extras=True)  # resolved Annotated types

Product.__annotate__ is None  # no PEP 649 evaluator under PEP 563
```

<!--
This is the PEP 563 caveat many codebases still hit because they use from __future__ import annotations.

When that future import is active, annotations are stored as strings and never evaluated at definition time. Product.__annotations__ gives you 'Name' and 'Price' as string values, not Annotated objects.

annotationlib.get_annotations with Format.VALUE returns those strings as-is — it does not magically evaluate them. Pass eval_str=True to resolve against module globals. Alternatively, get_type_hints always evaluates strings and with include_extras=True gives you the full Annotated types with metadata.

One more detail from our tests: under PEP 563 on Python 3.14, __annotate__ exists but is None. The compiler did not generate a PEP 649 lazy evaluator. hasattr returns True, but there is no callable to invoke.

The good news: PEP 649 is the default in Python 3.14 without that future import. You get lazy evaluation, a real __annotate__ callable, and Format.VALUE returns actual objects. PEP 563 is the legacy path you need to understand, not the direction of travel.
-->
