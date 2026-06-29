---
layout: default
class: code-center
---


# <span class="slide-title-code">annotated-types</span> contracts

<div class="divider-blue"></div>

<p class="slide-tagline"><code>BaseMetadata</code> + <code>GroupedMetadata</code> — two contracts.</p>

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

The get_metadata idiom we saw earlier is how library authors consume these contracts: isinstance against BaseMetadata, yield from GroupedMetadata, ignore everything else. annotated-types documents the pattern; Pydantic, SQLAlchemy, and Hypothesis all follow it.
-->
