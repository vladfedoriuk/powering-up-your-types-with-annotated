---
layout: default
class: code-center
---

# Filter constraints for <span class="slide-title-code">Depends</span>

<div class="divider-blue"></div>

<p class="slide-tagline"><code>get_metadata</code> yields <code>BaseMetadata</code> — <code>next()</code> picks the first <code>Depends</code>.</p>

```python {all|3|4-5|6-9|2,9}
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
This is exactly what a third-party package consuming annotated-types would have to do — scan the annotations, find the metadata it cares about, and act on it.

[click] It uses `get_type_hints` with `include_extras` set to `True` to inspect the parameters.

[click] We look for `Annotated` types

[click] find the first `Depends` metadata instance, and recursively resolve its callable.

[click] This gives us a dictionary of resolved dependencies that we can pass directly to our target function.
-->
