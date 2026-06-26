---
layout: default
class: code-center
---


# Call with injected deps

<div class="divider-blue"></div>

<p class="slide-tagline">Resolve dependency graph, call with <code>**deps</code>.</p>

```python
def handle_request(
    env: Annotated[str, Depends(settings)],
    user: Annotated[str, Depends(current_user)],
) -> str:
    return f"{user} via {env}"


with resolve_dependencies(handle_request) as deps:
    result = handle_request(**deps)
```

<!--
Here's the full usage pattern from our dependency injection snippet.

handle_request declares its dependencies via Annotated metadata — env comes from settings, user comes from current_user which itself depends on env. The resolver walks this graph recursively.

At call time, resolve_dependencies builds the injected keyword arguments, and you pass them to the handler. No global container, no magic decorators — just type hints and metadata introspection.
-->
