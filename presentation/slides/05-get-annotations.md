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
FORMAT.VALUE (default) — calls __annotate__(Format.VALUE); returns fully-evaluated Python objects. Raises NameError if a name is undefined at introspection time.

FORMAT.STRING — returns the annotation text exactly as written in source; no evaluation, no NameError risk. Useful for documentation tools or when you only need the name.

FORMAT.FORWARDREF — returns ForwardRef proxies for undefined names instead of raising NameError. Proxies resolve to the real type once the name is defined. Shown separately on the next slides.

Product: only 'price' and 'discount' — name lives on HasName. get_annotations never walks the MRO. That's the opposite of get_type_hints (next slide).

In Python 3.14, inspect.get_annotations IS annotationlib.get_annotations (same object).
-->
