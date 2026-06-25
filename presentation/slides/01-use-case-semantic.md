---
layout: default
---

# use case: semantic types

<div class="divider-blue"></div>

Name what data _is_ — disambiguate identical base types.

```python
from typing import Annotated
from sqlalchemy import Engine

ReaderEngine = Annotated[Engine, "Reader"]
WriterEngine = Annotated[Engine, "Writer"]
```

<!--
The first way people reach for Annotated is to create semantic types — types that name what data actually is, not just what Python type it happens to be.

Here's a real pattern from service-oriented architectures. You have two SQLAlchemy engines — one for reads, one for writes. They're both Engine objects. If you pass them around as plain Engine, there's nothing stopping you from accidentally using the writer where you meant the reader.

With Annotated, you create two distinct types: ReaderEngine and WriterEngine. They're still Engine under the hood — your type checker is happy, your IDE autocompletes correctly — but now they carry a semantic label that your dependency injection container, your service locator, or just your code reviewer can use to tell them apart.

The metadata here is just a string — "Reader" and "Writer" — but it could be anything: a dataclass, an enum, a custom marker object. Annotated doesn't care what the metadata is. It just carries it.

This is the first pillar: using Annotated to express what data means in your domain, without subclassing or wrapper types.
-->
