---
layout: default
class: code-center
---


# annotated internals

<div class="divider-blue"></div>

<p class="slide-tagline"><code>__origin__</code> vs <code>get_origin()</code> — two ways to unwrap.</p>

```python
from typing import Annotated, get_origin
from annotated_types import MinLen, MaxLen

Name = Annotated[str, MinLen(1), MaxLen(100)]

Name.__origin__    # → str
Name.__metadata__  # → (MinLen(1), MaxLen(100))

get_origin(Name)   # → Annotated  (not str!)
```

<!--
Let's look under the hood at how Annotated types work at runtime. Every Annotated type exposes two special attributes.

__origin__ gives you the unwrapped base type. In this example, Name.__origin__ is str. This is the actual type that your values are instances of at runtime.

__metadata__ gives you a tuple of all the metadata arguments, in the order they were provided. For Name, that's MinLen(1) and MaxLen(100).

Now here's a common gotcha that trips people up. The get_origin function from the typing module does NOT return the base type. It returns Annotated itself — the generic alias object. If you want the base type, you need to use __origin__ directly, or call get_args(Name)[0].

Two more important details about metadata. First, order matters. Annotated[int, MinLen(1), MaxLen(100)] is a different type from Annotated[int, MaxLen(100), MinLen(1)] — they're not equal. Second, metadata is never deduplicated. If you put MinLen(1) twice, you get it twice in the tuple. These are deliberate design choices that give library authors precise control.
-->
