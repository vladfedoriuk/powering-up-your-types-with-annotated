---
layout: default
class: code-center
---


# use case: framework metadata

<div class="divider-red"></div>

<p class="slide-tagline">Attach instructions for tools — Pydantic, FastAPI, SQLAlchemy.</p>

```python
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query

class SearchResult(BaseModel):
    total: Annotated[int, Field(ge=0)]

app = FastAPI()

@app.get("/search/")
def search(
    q: Annotated[str, Query(min_length=3)],
): ...
```

<!--
The second pillar is framework metadata — using Annotated to carry instructions that tools read at runtime.

Look at this FastAPI and Pydantic example. The SearchResult model has a total field: it's an int, but the Field metadata tells Pydantic to validate that it's greater than or equal to zero. The search endpoint has a query parameter q: it's a string, but the Query metadata tells FastAPI to enforce a minimum length of 3, and to read it from the query string.

This is where Annotated breaks the boundary between static analysis and runtime behavior. Your type checker sees int and str — it's happy, it can reason about your code. But at runtime, Pydantic and FastAPI see the metadata objects — Field and Query — and use them to validate, serialize, and generate OpenAPI documentation.

The key insight is that each framework reads only the metadata it understands and silently ignores the rest. You can stack metadata from Pydantic, FastAPI, SQLAlchemy, and your own custom tools on the same type, and they all coexist peacefully. This is the composability that makes Annotated so powerful.
-->
