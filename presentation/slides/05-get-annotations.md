---
layout: default
class: code-center
---


# <span class="slide-title-code">annotationlib.get_annotations</span>

<div class="divider-red"></div>

<p class="slide-tagline">Three formats — evaluated objects, source strings, or forward-reference proxies.</p>

```python
from annotationlib import Format, ForwardRef, get_annotations

get_annotations(HasName, format=Format.VALUE)
# {'name': Annotated[str, MinLen(1), MaxLen(100)]}   ← evaluated

get_annotations(HasName, format=Format.STRING)
# {'name': 'Name'}                                   ← source text, no eval


class Early:
    sibling: Pending  # not yet defined


get_annotations(Early, format=Format.FORWARDREF)
# {'sibling': ForwardRef('Pending')}                 ← proxy, no NameError
```

<!--
The new `annotationlib` API lets you retrieve annotations in three different formats.

`Format.VALUE` gives you fully evaluated Python objects. `Format.STRING` returns the raw source text as written. And `Format.FORWARDREF` returns proxy objects instead of raising a `NameError` if a type is not defined yet.

This is highly useful for library code that needs to inspect types before they are fully declared.
-->
