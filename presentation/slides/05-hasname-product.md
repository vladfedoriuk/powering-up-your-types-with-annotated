---
layout: default
class: code-center
---


# Example classes

<div class="divider-blue"></div>

```python
from decimal import Decimal
from typing import Annotated

from annotated_types import Ge, Gt, Le, MaxLen, MinLen

Name = Annotated[str, MinLen(1), MaxLen(100)]
Price = Annotated[Decimal, Gt(0)]
Percentage = Annotated[Decimal, Gt(0), Le(100)]


class HasName:
    name: Name


class Product(HasName):
    price: Price
    discount: Percentage | None
```

<!--
Reused through this section for get_annotations and get_type_hints demos. Same as snippets/annotations_introspection.py.

HasName declares name: Name. Product adds price and discount. Three annotated fields across the hierarchy; only two declared on Product itself — that gap is the point when comparing get_annotations (own only) vs get_type_hints (MRO merge).
-->
