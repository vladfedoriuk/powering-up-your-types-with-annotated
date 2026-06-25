---
layout: default
---


# get_type_hints vs get_annotations

<div class="divider-red"></div>

<p class="slide-tagline">Pick the right introspection API.</p>

| | `get_type_hints` | `get_annotations` |
|---|---|---|
| strips `Annotated` | yes (default) | no |
| keep metadata | `include_extras=True` | always |
| merges MRO | yes | no |
| evaluates strings | always | `eval_str=True` |
| since | python 3.5 | python 3.14 |

<!--
Now let's compare the two main APIs for getting annotations from Python objects, since choosing the right one matters for Annotated-aware code.

typing.get_type_hints has been around since Python 3.5. By default, it strips Annotated wrappers — you just get the base type. To keep the metadata, you need to pass include_extras=True. It always evaluates string annotations, and it merges annotations across the entire method resolution order — so you see parent class annotations too.

annotationlib.get_annotations is new in Python 3.14. It never strips Annotated metadata. It only returns own annotations, not inherited ones. It doesn't evaluate strings by default — you need to pass eval_str=True. And it has the Format parameter: VALUE gives you actual objects, STRING gives you source text, and FORWARDREF gives you proxy objects that don't raise NameError when names are undefined.

In Python 3.14, inspect.get_annotations is literally the same function as annotationlib.get_annotations — they point to the same object.

For Annotated-aware code, use get_type_hints with include_extras=True. For format-controlled access to own annotations, use get_annotations.
-->
