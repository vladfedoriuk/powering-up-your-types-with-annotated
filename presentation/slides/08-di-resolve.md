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
get_metadata is the idiom we just saw — yields BaseMetadata, unpacks GroupedMetadata composites.

next() picks the first Depends from that stream. None if no Depends on this parameter — the type checker sees only the base type and is unaffected.

Recursion handles transitive dependencies: endpoint depends on db_url which depends on config — resolve_dependencies walks the whole chain. No global registry — just type hints and metadata introspection.

This is the same isinstance dispatch that Pydantic and SQLAlchemy use. The only difference is what they're looking for.
-->
