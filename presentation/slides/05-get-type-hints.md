---
layout: default
class: code-center
---


# <span class="slide-title-code">typing.get_type_hints</span>

<div class="divider-red"></div>

<p class="slide-tagline">Merges MRO, resolves forward refs — strips <code>Annotated</code> unless <code>include_extras=True</code>.</p>

```python
from typing import get_type_hints

get_type_hints(Product)
# {'name': str, 'price': Decimal, ...}  ← stripped, full MRO

get_type_hints(Product, include_extras=True)
# {'name': Name, 'price': Price, ...}  ← Annotated preserved
```

<!--
For general application code, the `get_type_hints` function is often what you'll want instead.

Unlike the low-level `get_annotations` API, it automatically traverses the `MRO` to collect inherited types and resolves all forward references.

One important detail: by default, it strips `Annotated` wrappers away. You have to pass the `include_extras` flag to keep the metadata intact.
-->
