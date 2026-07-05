---
layout: default
class: code-center
---


# <span class="slide-title-code">BaseMetadata</span> + <span class="slide-title-code">GroupedMetadata</span>

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
The library defines two simple contracts: `BaseMetadata` and `GroupedMetadata`.

`BaseMetadata` is the base class for simple constraints, and `GroupedMetadata` is a protocol for composite ones, like `Interval` which yields `Gt` and `Lt`.

These contracts let any library safely scan type annotations without having to import or know about specific third-party types they don't own.
-->
