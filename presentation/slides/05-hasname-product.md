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
To demonstrate these runtime tools, we'll use these simple classes.

The first class has a `name` attribute, and the `Product` class inherits from it, adding `price` and an optional `discount`.

Notice that only `price` and `discount` are defined directly on the `Product` class. This distinction will be important in the next few slides.
-->
