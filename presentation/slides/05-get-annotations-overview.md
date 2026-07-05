---
layout: default
class: code-center
---


# Read annotations with the API

<div class="divider-red"></div>

<p class="slide-tagline">New in Python 3.14 — supersedes <code>inspect.get_annotations()</code>. Low-level tool; <code>typing.get_type_hints()</code> builds on top.</p>

```python
import annotationlib

# Preferred — own annotations only, never traverses MRO
annotationlib.get_annotations(HasName)
# {'name': Annotated[str, MinLen(1), MaxLen(100)]}

# Avoid __annotations__ directly — it has edge cases on older Pythons
HasName.__annotations__
# {'name': Annotated[str, MinLen(1), MaxLen(100)]}

# Use the API instead:
#   annotationlib.get_annotations()  Python 3.14+
#   inspect.get_annotations()        Python 3.10+
```

<!--
To read annotations, avoid accessing the raw `__annotations__` dictionary directly, as it has inconsistent behaviors on older Python versions.

Instead, use `annotationlib.get_annotations` in Python 3.14+, or `inspect.get_annotations` in Python 3.10+.

Keep in mind that these APIs only return the annotations defined directly on the class itself — they do not walk the MRO to merge parent class annotations.
-->
