---
layout: default
class: code-center
---


# The fix — <span class="slide-title-code">TypeForm</span>

<div class="divider-red"></div>

<p class="slide-tagline">PEP 747 — accepted for Python 3.15. Backport: <code>typing_extensions.TypeForm</code>.</p>

````md magic-move {lines: true}

```python
# Before — rejects Annotated
def register_value(svc_type: type[T], value: T) -> None: ...


register_value(Annotated[int, "x"], 42)  # ✗ type error
```

```python
# After — PEP 747, Python 3.15+
from typing import TypeForm  # or: from typing_extensions import TypeForm


def register_value(svc_type: TypeForm[T], value: T) -> None: ...


register_value(Annotated[int, "x"], 42)  # ✓ OK
```

````

<!--
A possible solution here is `TypeForm`, introduced in PEP 747 and landing in Python 3.15.

While `type[T]` only accepts concrete classes, `TypeForm[T]` accepts any valid type expression, including `Annotated` types.

Major type checkers have started supporting this experimentally today. If you have a similar use case where you need to pass type expressions around, `TypeForm` is the tool you want to look at.
-->
