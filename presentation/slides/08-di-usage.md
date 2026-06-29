---
layout: default
class: code-center
---


# Call with injected deps

<div class="divider-blue"></div>

<p class="slide-tagline">Resolve dependency graph, call with <code>**deps</code>.</p>

```python
def config() -> str:
    return "prod"

def db_url(env: Annotated[str, Depends(config)]) -> str:
    return f"db://{env}"

def endpoint(url: Annotated[str, Depends(db_url)]) -> str:
    return f"connected to {url}"


deps = resolve_dependencies(endpoint)
endpoint(**deps)  # "connected to db://prod"
```

<!--
Here's the full usage pattern from our dependency injection snippet.

handle_request declares its dependencies via Annotated metadata — env comes from settings, user comes from current_user which itself depends on env. The resolver walks this graph recursively.

At call time, resolve_dependencies builds the injected keyword arguments, and you pass them to the handler. No global container, no magic decorators — just type hints and metadata introspection.
-->
