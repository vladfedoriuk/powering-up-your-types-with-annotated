---
layout: default
---

# annotated internals

<div class="divider-blue"></div>

```python
from typing import Annotated, get_origin
from annotated_types import MinLen, MaxLen

Name = Annotated[str, MinLen(1), MaxLen(100)]

Name.__origin__    # → str
Name.__metadata__  # → (MinLen(1), MaxLen(100))

get_origin(Name)   # → Annotated  (not str!)
```

`__origin__` is the base type. `get_origin()` returns `Annotated` itself.

<!--
Let's look under the hood at how Annotated types work at runtime. Every Annotated type exposes two special attributes.

__origin__ gives you the unwrapped base type. In this example, Name.__origin__ is str. This is the actual type that your values are instances of at runtime.

__metadata__ gives you a tuple of all the metadata arguments, in the order they were provided. For Name, that's MinLen(1) and MaxLen(100).

Now here's a common gotcha that trips people up. The get_origin function from the typing module does NOT return the base type. It returns Annotated itself — the generic alias object. If you want the base type, you need to use __origin__ directly, or call get_args(Name)[0].

Two more important details about metadata. First, order matters. Annotated[int, MinLen(1), MaxLen(100)] is a different type from Annotated[int, MaxLen(100), MinLen(1)] — they're not equal. Second, metadata is never deduplicated. If you put MinLen(1) twice, you get it twice in the tuple. These are deliberate design choices that give library authors precise control.
-->

---
layout: default
---

# nested annotated — flattening

<div class="divider-blue"></div>

````md magic-move {lines: true}

```python
# Nested Annotated types are flattened — innermost first
inner = Annotated[int, MinLen(1)]
outer = Annotated[inner, MaxLen(100)]

outer == Annotated[int, MinLen(1), MaxLen(100)]  # True
outer.__metadata__  # (MinLen(1), MaxLen(100))
```

```python
# Through a PEP 695 type alias — NOT flattened
type AliasedInner = Annotated[int, MinLen(1)]
outer = Annotated[AliasedInner, MaxLen(100)]

outer == Annotated[int, MinLen(1), MaxLen(100)]  # False!
outer.__metadata__  # (MaxLen(100),)  ← only outer
```

````

<!--
There's an important subtlety with nested Annotated types that affects library authors building constraint resolvers.

When you nest Annotated directly — wrapping an Annotated type inside another Annotated — Python flattens them automatically. The inner metadata comes first, the outer metadata comes after. So Annotated of Annotated[int, MinLen(1)] with MaxLen(100) is exactly the same as Annotated[int, MinLen(1), MaxLen(100)]. They're the same type with the same metadata tuple.

Now watch what happens when the inner type is reached through a PEP 695 type alias — the type statement. In this case, flattening does NOT happen. The compiler avoids forcing evaluation of lazy aliases, so the outer Annotated sees only one argument — the alias object itself — and cannot introspect inside it.

This means outer.__metadata__ is just (MaxLen(100),) — only the outer metadata is visible. The inner MinLen(1) is hidden inside the alias.

This matters for libraries that walk the metadata chain. If you're building a constraint resolver, you need to be aware that TypeAliasType boundaries are opaque and won't automatically flatten.
-->
