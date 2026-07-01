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
This is what it looks like in practice. We have three simple functions, with dependencies chain-linked to one another.

We run `resolve_dependencies(endpoint)`. Our code walks the tree, runs `config`, then `db_url`, and resolves the final arguments.

We get our injected parameters as keyword arguments, ready to call the endpoint.
-->
