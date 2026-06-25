---
layout: default
class: code-center
---


# the fix — TypeForm

<div class="divider-red"></div>

<p class="slide-tagline">One-word fix — <code>type[T]</code> → <code>TypeForm[T]</code>.</p>

````md magic-move {lines: true}

```python
# Before — rejects Annotated
def register_value(svc_type: type[T], value: T) -> None: ...

register_value(Annotated[int, "x"], 42)  # ✗ type error
```

```python
# After — accepts any type form
from typing import TypeForm

def register_value(svc_type: TypeForm[T], value: T) -> None: ...

register_value(Annotated[int, "x"], 42)  # ✓ OK
```

````

<!--
PEP 747's TypeForm fixes this problem. You change type[T] to TypeForm[T] — literally one word. TypeForm[T] is a supertype of type[T], so concrete classes still work exactly as before. But now Annotated[int, "x"] is also accepted.

All five major type checkers accept the TypeForm version. This PEP was accepted for Python 3.15, and a backport is available in typing_extensions for earlier versions.
-->
