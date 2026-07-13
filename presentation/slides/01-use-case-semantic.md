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
Imagine you have a replicated database setup with separate reader and writer instances. You need to annotate an engine parameter in a function, but plain `Engine` doesn't tell you which one you're using.

`Annotated` fixes that. `ReaderEngine` and `WriterEngine` are the same runtime type with different labels. The type checker sees `Engine`; the code reviewer sees the intention.

The metadata is just a string — it could be anything.
-->
