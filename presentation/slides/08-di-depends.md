---
layout: default
class: code-center
---


# Auto-wiring with <span class="slide-title-code">Annotated</span>

<div class="divider-blue"></div>

<p class="slide-tagline">Metadata-driven autowiring — <code>Depends</code> as <code>BaseMetadata</code>.</p>

```python
from dataclasses import dataclass
from annotated_types import BaseMetadata


@dataclass(frozen=True)
class Depends(BaseMetadata):
    dependency: Callable


# usage — metadata on the parameter annotation
def current_user(env: Annotated[str, Depends(settings)]) -> str: ...
```

<!--
First, we need a marker. We define a simple `Depends` dataclass that inherits from `BaseMetadata`.

Then, we annotate our function parameters with it, like telling `current_user` to get its `env` string from `settings`.

Next, we need the function that actually resolves these dependencies at runtime.
-->
