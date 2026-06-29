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
Now let's see how these contracts enable autowiring with Annotated — not a DI framework, just metadata introspection.

The Depends class is a frozen dataclass that subclasses BaseMetadata. It carries a callable dependency. This is the metadata marker.

The _resolve function scans a function's type hints using get_type_hints with include_extras=True. For each parameter, it checks if the hint is an Annotated type. If it is, it walks the metadata tuple looking for Depends instances. When it finds one, it recursively resolves the dependency and stores the result in a dictionary.

This is about twenty lines of code. There's no framework magic here — just the standard Annotated introspection pattern we've been exploring. The type checker sees only the base type of each parameter, so it's completely type-safe. This is intentionally minimal to show that the pattern itself is simple.
-->
