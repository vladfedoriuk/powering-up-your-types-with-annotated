---
layout: default
class: code-center
---


# The <span class="slide-title-code">get_metadata</span> idiom

<div class="divider-red"></div>

<p class="slide-tagline">Suggested by <code>annotated-types</code> — walk metadata that implements <code>BaseMetadata</code> or <code>GroupedMetadata</code>.</p>

```python
from typing import Annotated, get_args, get_origin
from annotated_types import BaseMetadata, GroupedMetadata


def get_metadata(tp):
    assert get_origin(tp) is Annotated
    for arg in get_args(tp)[1:]:  # [0] is the base type
        if isinstance(arg, BaseMetadata):
            yield arg
        elif isinstance(arg, GroupedMetadata):
            yield from arg  # e.g. Interval → Gt + Lt
```

<!--
This is not a stdlib API — it is the consumption idiom annotated-types documents for library authors. Walk an Annotated type's metadata tuple and dispatch on the two contracts the package defines.

BaseMetadata covers simple constraints: Gt, Le, MinLen, and so on. GroupedMetadata covers composites that unpack via __iter__ — Interval yields Gt and Lt, Len yields MinLen and MaxLen.

get_args(tp)[0] is always the base type; everything from index 1 onward is metadata. Your library yields what it understands and ignores the rest — that is the loose coupling.

Pydantic, SQLAlchemy, and Hypothesis all follow variants of this same isinstance loop. The annotated-types test suite shows the reference implementation. If your metadata objects implement BaseMetadata or GroupedMetadata, any consumer using this idiom can read them without importing your types.
-->
