---
layout: default
class: code-center
---


# Use case: semantic types

<div class="divider-blue"></div>

<p class="slide-tagline">Same type — different meaning.</p>

```python
from typing import Annotated
from sqlalchemy import Engine

ReaderEngine = Annotated[Engine, "Reader"]
WriterEngine = Annotated[Engine, "Writer"]
```

<!--
Two SQLAlchemy engines — reader and writer. Both typed as Engine. Nothing stops you from mixing them up.

Annotated fixes that. You get ReaderEngine and WriterEngine — same runtime type, different meaning. The type checker sees Engine; your code reviewer sees which one you actually meant.

The metadata here is just a string. It could be anything — Annotated doesn't care.
-->
