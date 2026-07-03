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
For our last layer, documentation. annotated-doc adds a Doc object right inside the type — it's built on the revoked PEP 727, championed by Sebastian Ramirez, and it already powers Typer and FastAPI's docs.

Doc has to be the first item in the annotation, and applied directly to the constant or argument, not through an alias — otherwise doc tools won't pick it up.
-->
