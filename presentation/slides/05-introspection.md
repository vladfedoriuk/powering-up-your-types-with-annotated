---
layout: default
---

# introspecting annotated

<div class="divider-red"></div>

The `get_constraints()` pattern — used by Pydantic and other consumers.

```python
from typing import Annotated, get_args, get_origin
from annotated_types import BaseMetadata, GroupedMetadata

def get_constraints(tp):
    assert get_origin(tp) is Annotated
    for arg in get_args(tp)[1:]:        # [0] is the base type
        if isinstance(arg, BaseMetadata):
            yield arg
        elif isinstance(arg, GroupedMetadata):
            yield from arg              # e.g. Interval → Gt + Lt
```

<!--
Here's the canonical pattern that Pydantic and other Annotated-aware libraries use to extract constraints from type annotations.

The function takes an Annotated type and yields all the BaseMetadata and GroupedMetadata objects from its metadata tuple.

The key insight is in how get_args works. The first element, at index zero, is the base type — str, int, Decimal, whatever your values actually are. Everything from index one onwards is metadata.

For simple constraints like Gt or MinLen, they're instances of BaseMetadata, so you yield them directly.

For grouped constraints like Interval or Len, they implement the GroupedMetadata protocol, which means they're iterable. Interval yields Gt and Lt. Len yields MinLen and MaxLen. So you yield from them to unpack the individual constraints.

This is the contract that annotated-types establishes for the whole ecosystem. If you're a constraint, you're either BaseMetadata or GroupedMetadata. Libraries do isinstance checks against these two contracts, and the whole system stays loosely coupled.
-->

---
layout: default
---

# get_type_hints vs get_annotations

<div class="divider-red"></div>

|  | `get_type_hints` | `get_annotations` |
|---|---|---|
| strips `Annotated` | yes (default) | no |
| keep metadata | `include_extras=True` | always |
| merges MRO | yes | no (own only) |
| evaluates strings | always | `eval_str=True` |
| format support | — | VALUE / FORWARDREF / STRING |
| since | python 3.5 | python 3.14 |

<!--
Now let's compare the two main APIs for getting annotations from Python objects, since choosing the right one matters for Annotated-aware code.

typing.get_type_hints has been around since Python 3.5. By default, it strips Annotated wrappers — you just get the base type. To keep the metadata, you need to pass include_extras=True. It always evaluates string annotations, and it merges annotations across the entire method resolution order — so you see parent class annotations too.

annotationlib.get_annotations is new in Python 3.14. It never strips Annotated metadata. It only returns own annotations, not inherited ones. It doesn't evaluate strings by default — you need to pass eval_str=True. And it has the Format parameter: VALUE gives you actual objects, STRING gives you source text, and FORWARDREF gives you proxy objects that don't raise NameError when names are undefined.

In Python 3.14, inspect.get_annotations is literally the same function as annotationlib.get_annotations — they point to the same object.

For Annotated-aware code, use get_type_hints with include_extras=True. For format-controlled access to own annotations, use get_annotations.
-->
