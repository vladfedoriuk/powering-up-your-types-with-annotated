---
layout: default
class: code-center
---


# Aliases block flattening

<div class="divider-blue"></div>

<p class="slide-tagline">PEP 695 <code>type</code> aliases are <em>lazy</em> — outer <code>Annotated</code> cannot see inside until evaluated.</p>

```python
from typing import Annotated
from annotated_types import MinLen, MaxLen

type Inner = Annotated[int, MinLen(1)]

Annotated[Inner, MaxLen(100)].__metadata__
# (MaxLen(100),)  ← MinLen(1) is hidden inside Inner
```

<!--
Put the inner Annotated behind a PEP 695 type alias and flattening stops. PEP 695 aliases are lazy — the compiler does not evaluate them eagerly, so the outer Annotated sees one opaque argument instead of the inner metadata tuple.

The same rule applies to generic aliases (Band[int]) — mention in one sentence if the room asks; no separate slide.

Library authors cannot walk __metadata__ alone; they must evaluate the alias to recover inner constraints. Mention call_evaluate_function on alias.evaluate_value only if someone asks.
-->
