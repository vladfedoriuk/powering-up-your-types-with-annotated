---
layout: default
---

# annotated is not a type

<div class="divider-red"></div>

A special form — not assignable to `type[T]`.

```python
from typing import Annotated

type(Annotated[int, "x"])
# <class 'typing._AnnotatedAlias'>

isinstance(Annotated[int, "x"], type)
# False
```

<!--
Here's something that surprises a lot of people: Annotated is not a type. It's what the typing spec calls a "special form" — an object with special meaning to the type system, comparable to a keyword rather than a concrete class.

At runtime, Annotated[int, "x"] is a typing._AnnotatedAlias object. It's not an instance of type. The isinstance check returns False.

The typing spec is explicit about this: "An attempt to call Annotated, whether parameterized or not, should be treated as a type error by type checkers."

This has a real consequence for libraries: if your API accepts type[T], you cannot pass Annotated[int, "x"]. Type checkers will reject it.
-->

---
layout: default
---

# the svcs problem

<div class="divider-red"></div>

A real-world collision — `Annotated` passed as `type[T]`.

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

---
layout: default
---

# the fix — TypeForm

<div class="divider-red"></div>

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
