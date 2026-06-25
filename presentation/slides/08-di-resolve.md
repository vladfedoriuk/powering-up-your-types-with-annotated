---
layout: default
class: code-center
---


# Resolve dependencies

<div class="divider-blue"></div>

<p class="slide-tagline">Context manager yields resolved kwargs dict.</p>

```python
@contextmanager
def resolve_dependencies(fn: Callable) -> Iterator[dict[str, Any]]:
    yield _resolve(fn)
```

<!--
The resolve_dependencies context manager wraps _resolve so you can inject dependencies at call time.

It yields a dictionary mapping parameter names to resolved values. The generic signature preserves the callable's type parameters, so type checkers can still reason about the function being resolved.

This is the bridge between introspection and actual invocation — you resolve once, then pass the result as keyword arguments to your handler.
-->
