---
layout: default
class: code-center
---

# Auto-wiring with <span class="slide-title-code">Annotated</span>

<div class="divider-blue"></div>

<p class="slide-tagline">Metadata-driven autowiring — <code>Depends</code> as <code>BaseMetadata</code>.</p>

```python{all|5-7|10-11|all}
from dataclasses import dataclass
from annotated_types import BaseMetadata


@dataclass
class Depends(BaseMetadata):
    dependency: Callable


# usage — metadata on the parameter annotation
def current_user(env: Annotated[str, Depends(settings)]) -> str: ...
```

<!--
What if `annotated-types` shipped `Depends` as a primitive?

[click] We define a simple `Depends` dataclass that inherits from `BaseMetadata`.

[click] Then, we annotate our function parameters with it, like telling `current_user` to get its `env` string from `settings`.

[click] Next, we need the function that actually resolves these dependencies at runtime.
-->
