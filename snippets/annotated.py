from typing import Annotated

import svcs
from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel
from pydantic.fields import Field
from sqlalchemy import Engine, create_engine

ReaderEngine = Annotated[Engine, "Reader"]
WriterEngine = Annotated[Engine, "Writer"]

registry = svcs.Registry()
registry.register_value(
    ReaderEngine,
    create_engine(url="postgresql+asyncpg://user:password@reader/dbname"),
)
registry.register_value(
    WriterEngine,
    create_engine(url="postgresql+asyncpg://user:password@writer/dbname"),
)

app = FastAPI()


class SearchResult(BaseModel):
    total: Annotated[int, Field(description="Total number of results", ge=0)]


class SomeDep: ...


@app.get("/search/")
def search(  # type: ignore [empty-body]
    _q: Annotated[str, Query(min_length=3)],
    _some_dep: Annotated[
        SomeDep,
        Depends(...),
    ],
) -> SearchResult: ...
