---
layout: default
class: code-center
---


# the svcs problem

<div class="divider-red"></div>

<p class="slide-tagline">Real collision — <code>Annotated</code> passed as <code>type[T]</code>.</p>

```python
def register_value(svc_type: type[T], value: T) -> None: ...

register_value(Annotated[int, "my_int"], 42)
# ↑ type error in mypy, pyright, ty, pyrefly
```

<!--
This hit a real library in production. svcs is Hynek Schlawack's service locator library. Its documentation recommended using Annotated types as registry keys — Annotated[int, "my_int"] as the key to register multiple values for the same base type.

This pattern worked fine at runtime. But when Pyright 1.1.350 tightened spec conformance, it correctly rejected it. mypy, ty, and pyrefly all reject it too.

Hynek chose to warn users away from the pattern rather than weaken svc_type to Any. The broader lesson here is that any library passing Annotated as type[T] will hit this wall.
-->
