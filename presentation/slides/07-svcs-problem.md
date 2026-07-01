---
layout: default
class: code-center
---


# The problem

<div class="divider-red"></div>

<p class="slide-tagline">Real collision — <code>Annotated</code> passed as <code>type[T]</code>.</p>

```python
def register_value(svc_type: type[T], value: T) -> None: ...


register_value(Annotated[int, "my_int"], 42)
# ↑ type error in mypy, pyright, ty, pyrefly
```

<!--
This is a case that a popular library stumbled upon in real life.

The service locator library `svcs` recommended using Annotated types as registry keys. It worked fine at runtime, but type checkers started raising errors because the registration function expected `type[T]`.

Since `Annotated` is a special form, type checkers were right to complain. Let's see how we can fix this.
-->
