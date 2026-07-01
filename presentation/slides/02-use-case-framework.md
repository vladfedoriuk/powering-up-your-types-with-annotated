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
The second use case is framework metadata — attaching instructions for external libraries to read.

Here, Pydantic checks if `total` is at least zero, and FastAPI expects the query parameter `q` to be at least three characters.

Static typing handles the `int` and `str` checks, while runtime libraries read the annotations to validate or even document our API.
-->
