---
layout: default
---

# the contracts

<div class="divider-blue"></div>

```python
@dataclass(frozen=True)
class BaseMetadata:
    """Base for simple constraints: Gt, Le, MinLen, …"""

class GroupedMetadata(Protocol):
    def __iter__(self) -> Iterator[BaseMetadata]: ...
    # Interval → Gt + Lt, Len → MinLen + MaxLen
```

<!--
The annotated-types library establishes two simple contracts that all constraint metadata follows.

BaseMetadata is a frozen dataclass that serves as the base for simple constraints like Gt, Le, and MinLen. Libraries do isinstance checks against this base to find constraints they understand.

GroupedMetadata is a protocol that yields BaseMetadata objects. It's used for composite constraints like Interval, which yields Gt and Lt, or Len, which yields MinLen and MaxLen.

The get_constraints function we saw on the previous slide relies entirely on these two contracts. It checks isinstance against BaseMetadata for simple constraints, and it yields from GroupedMetadata for composite ones. This is how the whole ecosystem stays loosely coupled.
-->

---
layout: default
---

# DI with Annotated

<div class="divider-blue"></div>

```python
@dataclass(frozen=True)
class Depends(BaseMetadata):
    dependency: Callable

def _resolve(fn):
    injected = {}
    for name, hint in get_type_hints(fn, include_extras=True).items():
        if get_origin(hint) is not Annotated:
            continue
        for meta in get_args(hint)[1:]:
            if isinstance(meta, Depends):
                injected[name] = meta.dependency(**_resolve(meta.dependency))
    return injected
```

<!--
Now let's see how these contracts enable dependency injection with Annotated.

The Depends class is a frozen dataclass that subclasses BaseMetadata. It carries a callable dependency. This is the metadata marker.

The _resolve function scans a function's type hints using get_type_hints with include_extras=True. For each parameter, it checks if the hint is an Annotated type. If it is, it walks the metadata tuple looking for Depends instances. When it finds one, it recursively resolves the dependency and stores the result in a dictionary.

This is about twenty lines of code. There's no framework magic here — just the standard Annotated introspection pattern we've been exploring. The type checker sees only the base type of each parameter, so it's completely type-safe. This is intentionally minimal to show that the pattern itself is simple.
-->

---
layout: default
---

# production implementations

<div class="divider-blue"></div>

- `uncalled-for` — standalone typed DI, async lifecycle
- `FastDepends` — FastAPI's DI extracted, sync/async, Provider overrides
- `FastMCP` — production consumer of `uncalled-for`

<!--
Our twenty-line toy works, but production dependency injection engines add layers of complexity that the toy ignores.

uncalled-for is a standalone typed DI engine built entirely on Annotated metadata. It adds async context manager lifecycle support and dependency deduplication, so the same dependency is resolved once per call rather than multiple times.

FastDepends is FastAPI's dependency injection system extracted into a pure Python library. It supports both sync and async, adds Provider-based overriding for tests, and includes custom field support. It powers FastStream and Propan.

FastMCP is a production consumer of uncalled-for. Its CurrentContext, CurrentFastMCP, and TokenClaim are all Annotated metadata objects resolved at call time via async context managers.

The arc is the same: a twenty-line toy demonstrates the pattern, libraries like uncalled-for and FastDepends add production features, and frameworks like FastMCP consume them. But the mechanism underneath is always the same Annotated pattern.
-->
