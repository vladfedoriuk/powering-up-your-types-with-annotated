---
layout: default
class: code-center
---


# Filter constraints for <span class="slide-title-code">Depends</span>

<div class="divider-blue"></div>

<p class="slide-tagline"><code>get_metadata</code> yields <code>BaseMetadata</code> — <code>next()</code> picks the first <code>Depends</code>.</p>

```python
def resolve_dependencies(fn):
    injected = {}
    for name, hint in get_type_hints(fn, include_extras=True).items():
        if get_origin(hint) is not Annotated:
            continue
        dep = next((m for m in get_metadata(hint) if isinstance(m, Depends)), None)
        if dep is not None:
            injected[name] = dep.dependency(**resolve_dependencies(dep.dependency))
    return injected
```

<!--
Here is the resolver function. It uses `get_type_hints` with `include_extras=True` to inspect the parameters.

We look for `Annotated` types, find the first `Depends` metadata instance, and recursively resolve its callable.

This gives us a dictionary of resolved dependencies that we can pass directly to our target function.
-->
