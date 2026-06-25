---
layout: default
class: code-center
---


# Documentation: <span class="slide-title-code">annotated-doc</span>

<div class="divider-yellow"></div>

<p class="slide-tagline"><code>Doc</code> metadata inline in type signatures.</p>

```python
from annotated_doc import Doc

FIRST_ORDER_DISCOUNT: Annotated[
    Percentage,
    Doc("Discount percentage applied to the first reservation made by a guest"),
] = Decimal(15)
```

<!--
For our final layer, we look at documentation.

annotated-doc introduces the Doc metadata object, which was proposed in the revoked PEP 727. It allows you to document constants, parameters, or fields directly inside their types. Sebastian Ramirez championed this pattern, and it powers Typer and FastAPI's internal documentation rendering.
-->
