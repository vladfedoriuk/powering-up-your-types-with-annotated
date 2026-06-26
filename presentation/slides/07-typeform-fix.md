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
PEP 747 — "Annotating Type Forms" — was accepted for Python 3.15. A backport is available in typing_extensions today.

TypeForm[T] is a supertype of type[T]: concrete classes still work exactly as before. But now Annotated[int, "x"] is also a valid TypeForm[int] — no type error.

All five major type checkers (mypy, pyright, pyrefly, ty, pylance) accept the TypeForm version.

References:
- PEP 747: https://peps.python.org/pep-0747/
- TypeForm spec: https://typing.python.org/en/latest/spec/type-forms.html
- Python 3.15 docs: https://docs.python.org/3.15/library/typing.html#typing.TypeForm
-->
