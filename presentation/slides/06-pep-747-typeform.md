---
layout: default
class: code-center
---


# PEP 747 — <span class="slide-title-code">TypeForm</span>

<div class="divider-yellow"></div>

<p class="slide-tagline"><code>typeform[T]</code> accepts type expressions, not just classes.</p>

```python
from typing import TypeForm  # Python 3.15, or typing_extensions


def accepts_type_form(tp: TypeForm[int]) -> None: ...


accepts_type_form(int)  # ✓ OK
accepts_type_form(Annotated[int, "tag"])  # ✓ OK
```

<!--
Before we dive into the next section, let me briefly mention PEP 747 — TypeForm.

This is a new special form that was accepted for Python 3.15. It solves a specific problem: how do you annotate a function parameter that should accept any type expression, not just concrete classes?

TypeForm[T] is a supertype of type[T]. A type[int] is accepted wherever TypeForm[int] is expected. But TypeForm also accepts things that type does not — like Annotated[int, "tag"], or Union[int, str], or any parameterized generic.

Until Python 3.15 ships, typing_extensions provides the backport.

We'll see why this matters in the next section, where we look at what happens when libraries try to use Annotated types as type[T] parameters.
-->
