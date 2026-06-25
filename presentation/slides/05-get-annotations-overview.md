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
Source: https://docs.python.org/3/howto/annotations.html (Larry Hastings)

__annotations__ is the raw underlying dict. On Python 3.10+ getattr(cls, "__annotations__") is safe — it always returns the class's own dict (or {}). On Python 3.9 and earlier, accessing __annotations__ on a class with no annotations of its own would return the parent's dict instead of {}. The fix: use __dict__.get('__annotations__', None) for classes, and getattr(o, '__annotations__', None) for everything else.

annotationlib.get_annotations() handles all of this for you — prefer it over raw access. Next slide shows the three Format values in action.
-->
