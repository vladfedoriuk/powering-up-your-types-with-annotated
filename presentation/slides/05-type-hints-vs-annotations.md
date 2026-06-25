---
layout: default
---


# Three ways to read annotations

<div class="divider-red"></div>

<p class="slide-tagline">Different contracts — pick the API that matches your job.</p>

| | get_type_hints | get_annotations |
|---|---|---|
| strips `Annotated` | yes (default) | no |
| keep metadata | `include_extras=True` | always |
| merges MRO | yes | no (own only) |
| `format=` control | — | value / string / forwardref |
| evaluates strings | always | `eval_str=True` |
| since | Python 3.5 | Python 3.14 (`annotationlib`) |

<!--
Here is the cheat sheet tying the last two slides together.

get_type_hints is the framework author's tool — DI, validation, anything that needs fully resolved types across inheritance. get_annotations is the introspection author's tool — own annotations, format control, no silent MRO merge.

The evolution across Python versions: raw __annotations__ before 3.10 had inheritance bugs. inspect.get_annotations from 3.10 to 3.13 was the safe own-only API. annotationlib.get_annotations in 3.14 adds Format and becomes what inspect re-exports.

For Annotated-aware libraries: get_type_hints with include_extras=True for runtime resolution on callables and classes where you need the full MRO. get_annotations with format=Format.VALUE for precise own-field introspection. Never assume they are interchangeable.
-->
