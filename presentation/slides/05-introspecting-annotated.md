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
This is the recommended helper function to extract those constraints at runtime.

We verify that the type is indeed `Annotated`, and then iterate through its arguments. We yield simple constraints directly and unpack composite ones using the `GroupedMetadata` protocol.

This is basically the blueprint libraries like Pydantic or Hypothesis use under the hood.
-->
