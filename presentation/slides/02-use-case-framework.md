---
layout: default
class: code-center
---

# Use case: framework metadata

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
Here we're attaching instructions for external libraries to read.

`Pydantic` checks if `total` is at least zero, and `FastAPI` expects the query parameter to be at least three characters.

These libraries check both the types and the metadata — static typing only handles the integer and string checks, while runtime libraries additionally read the annotations to validate or even document our API.
-->
