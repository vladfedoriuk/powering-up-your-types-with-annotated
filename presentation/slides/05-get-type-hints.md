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
stdlib docs: https://docs.python.org/3/library/typing.html#typing.get_type_hints

Higher-level than get_annotations — built for frameworks that need fully resolved types on callables and classes.

What it changes vs raw annotations: evaluates ForwardRef and string annotations; merges base-class annotations via MRO (subclass wins); replaces Annotated[T, ...] with T unless include_extras=True; None defaults became unchanged since 3.11.

3.14: format= parameter aligned with annotationlib. Instances: use get_type_hints(type(obj)), not the instance.

Caution from docs: may execute arbitrary code in annotations when evaluating strings.

This is what our DI toy uses: get_type_hints(fn, include_extras=True). Pair with the previous slide: get_annotations for own-field introspection with format control; get_type_hints when you need inheritance merged and types resolved for runtime dispatch.
-->
