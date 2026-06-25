---
layout: default
---

# PEP 563 caveat

<div class="divider-yellow"></div>

`from __future__ import annotations` stores everything as strings.

```python
from __future__ import annotations
from typing import Annotated, get_type_hints
from annotated_types import MinLen, MaxLen, Gt

Name = Annotated[str, MinLen(1), MaxLen(100)]

class Product:
    name: Name
    price: Annotated[Decimal, Gt(0)]

Product.__annotations__
# {'name': 'Name', 'price': 'Annotated[Decimal, Gt(0)]'}  ← strings!

get_type_hints(Product, include_extras=True)
# {'name': Annotated[str, MinLen(1), MaxLen(100)], ...}    ← resolved
```

<!--
There's an important caveat when working with PEP 563 — the from __future__ import annotations statement that many projects use.

When this future import is active, Python stores all annotations as raw strings. It never evaluates them. So Product.__annotations__ gives you the dictionary with string values: 'Name' and 'Annotated[Decimal, Gt(0)]'.

If you call annotationlib.get_annotations with Format.VALUE, you get these strings as-is — it does not evaluate them. You need to pass eval_str=True to make it resolve the strings against the module globals.

Alternatively, typing.get_type_hints always evaluates strings — it was designed for this. With include_extras=True, you get the fully resolved Annotated types with all their metadata intact.

One more thing: under PEP 563, Python 3.14 sets __annotate__ to None rather than a callable function. This is because the compiler never generates the PEP 649 lazy evaluator when annotations are stored as strings. So if you're checking for __annotate__, be aware it exists but is None.

The good news is that PEP 649, which is the default in Python 3.14, fixes all of this with true lazy evaluation.
-->

---
layout: default
---

# PEP 747 — TypeForm

<div class="divider-yellow"></div>

Annotate functions that accept type-form objects.

```python
from typing import TypeForm  # Python 3.15, or typing_extensions

def accepts_type_form(tp: TypeForm[int]) -> None: ...

# TypeForm[T] is a supertype of type[T]:
accepts_type_form(int)                      # ✓ OK
accepts_type_form(Annotated[int, "tag"])     # ✓ OK
```

Accepted for Python 3.15. Backport: `typing_extensions.TypeForm`.

<arg_value><!--
Before we dive into the next section, let me briefly mention PEP 747 — TypeForm.

This is a new special form that was accepted for Python 3.15. It solves a specific problem: how do you annotate a function parameter that should accept any type expression, not just concrete classes?

TypeForm[T] is a supertype of type[T]. A type[int] is accepted wherever TypeForm[int] is expected. But TypeForm also accepts things that type does not — like Annotated[int, "tag"], or Union[int, str], or any parameterized generic.

Until Python 3.15 ships, typing_extensions provides the backport.

We'll see why this matters in the next section, where we look at what happens when libraries try to use Annotated types as type[T] parameters.
-->
