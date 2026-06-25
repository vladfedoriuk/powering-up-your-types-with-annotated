---
layout: default
class: code-center
---


# <span class="slide-title-code">Annotated</span> is not a type

<div class="divider-red"></div>

<p class="slide-tagline">Special form — not assignable to <code>type[T]</code>.</p>

```python
from typing import Annotated

type(Annotated[int, "x"])
# <class 'typing._AnnotatedAlias'>

isinstance(Annotated[int, "x"], type)
# False
```

<!--
Here's something that surprises a lot of people: Annotated is not a type. It's what the typing spec calls a "special form" — an object with special meaning to the type system, comparable to a keyword rather than a concrete class.

At runtime, Annotated[int, "x"] is a typing._AnnotatedAlias object. It's not an instance of type. The isinstance check returns False.

The typing spec is explicit about this: "An attempt to call Annotated, whether parameterized or not, should be treated as a type error by type checkers."

This has a real consequence for libraries: if your API accepts type[T], you cannot pass Annotated[int, "x"]. Type checkers will reject it.
-->
