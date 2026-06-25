---
layout: default
class: code-center
---


# nested annotated — flattening

<div class="divider-blue"></div>

<p class="slide-tagline">Direct nesting flattens; PEP 695 aliases do not.</p>

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
